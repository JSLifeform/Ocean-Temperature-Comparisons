import os
import numpy as np
import re
import pandas as pd
import panel as pn
from IPython.display import display
import time
import geopandas as gpd
from shapely import geometry
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# function to split files
def fileSplit(dataFile):
    
    #line to split files on
    fileEnd='END OF VARIABLES SECTION'
    
    #counter to delete last empty file
    fileCount = 1
    
    # create files
    def files():
        n = 0
        while True:
            n += 1
            fileCount = n
            yield open('tabular_data/%d.csv' % n, 'w')
    
    #creates and opens first file
    fileSystem=files()
    outFile=next(fileSystem)
    
    #loops through lines in file. If not end of df, writes line to file
    with open(dataFile) as inFile:
        for line in inFile:
            if fileEnd not in line:
                outFile.write(line)
            #if end of dataframe, write line to file and open now file    
            else:
                outFile.write(line)
                outFile=next(fileSystem)
                fileCount += 1
    
    #close and delete last empty file
    outFile.close()
    os.remove('tabular_data/%d.csv' % fileCount)




# Function to process(wording, ugh) processed files after original file has been split into processed files
def processSplit(fileName, shapesDF):
    #latitude and longitude variables
    latitude = ''
    longitude = ''
    lineCounter = 0
    df = []
    latColumn = []
    longColumn = []
    
    
    #opens file and reads lines
    file = open(fileName, 'r')
    for line in file:
        if 'Latitude' in line: 
            latitude = line
            lineCounter += 1
        elif 'Longitude' in line: 
            longitude = line
            lineCounter += 1
        elif 'UNITS' in line:
            df = pd.read_csv(fileName, header = lineCounter)
            break
        else:
            lineCounter += 1

    # split line on commas
    latitude = latitude.split(',')
    longitude = longitude.split(',')

    #select item from list with numerical lat/long value, strip whitespace
    latitude = latitude[2]
    longitude = longitude[2]
    latitude = float(latitude.strip())
    longitude = float(longitude.strip())
    
    
    #rename columns
    df = (df.rename(columns = {'m         ': 'Depth(m)', 'degrees C ': 'Temperature(C)', ' .3': 'Salinity(unitless)',
                              ' .4': 'Oxygen(µmol/kg)'}))
    #trim first and last useless rows from df, selects desired columns
    df = df.reindex(columns = ['Depth(m)', 'Temperature(C)', 'Salinity(unitless)', 'Oxygen(µmol/kg)'])
    df = df.iloc[1:(len(df)-2), :]
    
    # changes depth from string to float
#     df['Depth(m)']=pd.to_numeric(df['Depth(m)'], downcast='float')

    
    #loops to create latitude/longitude columns
    for i in range(len(df)):
        latColumn.append(latitude)
        longColumn.append(longitude)
    
    df['Latitude'] = latColumn
    df['Longitude'] = longColumn
    
    # turns values in dataframe to floats if possible
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # adds geospatial data to dataframe
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

    
    # line to return out of function if empty dataframe is provided, stops errors on gdf.iloc[0,:] line
    if gdf.empty: return gdf
    
    
    point = gdf.iloc[0, : ]
    for i in range(len(shapesDF)):
        shape = shapesDF.iloc[i, :]
        if point.geometry.within(shape.geometry):
#         if point['geometry'].within(shape['geometry']):
            gdf['zone'] = shape['zone']
            break
        else:
            continue
    file.close()
    return(gdf)



# function that loops through processed files in tabular_data folder and adds each to dataframe
def processFile(fileList, shapefile):
    shapesDF = shapefile
    df = []
    # loops through files
    for file in fileList:
        #ignores .gitkeep file to include folder in gitHub
        if file == '.gitkeep': continue
        #creates temporary datafram from each processed file
        addData = processSplit('tabular_data/%s' % file, shapesDF)
        #checks to see if anything is appended to df. If not, creates df with same dimensions as processed df's, then adds data
        if len(df) == 0:
            df = pd.DataFrame().reindex(columns = addData.columns)
        df = df.append(addData, ignore_index = True)
    
    # cleans processed files out of tabular_data for next data file to run
    for file in fileList:
        if file == '.gitkeep': continue
        os.remove('tabular_data/%s' %file)
            
            
    return df

# creates geopandas dataframe to cut up points and map
def latSplit(latitude):
    globeLat = gpd.GeoDataFrame(columns = ['zone', 'geometry'])
    for j in range(2):
        for i in range(int(180/latitude)):
            p1 = [(j * 180)-180, (i*latitude)-90.00000]
            p2 = [(j * 180), (i*latitude)-90.00000]
            p3 = [(j * 180), ((i+1)*latitude)-90.00000]
            p4 = [(j * 180)-180, ((i+1)*latitude)-90.00000]
            pointList = [p1, p2, p3, p4, p1]
            poly = geometry.Polygon(pointList)
            if j == 0:
                globeLat.loc[i] = [(str(i*latitude-90) + 'W') , poly]
            else:
                globeLat.loc[i + (180/latitude)] = [(str(i*latitude-90) + 'E') , poly]
            globeLat.append({'zone': (str((i*latitude-90))) , 'geometry': poly}, ignore_index = True)
    return globeLat
        

# pulls list of files in data/ folder
def processFolder(folder, shapefile = latSplit(5)):
    uncutFiles = os.listdir(folder)
    shapesDF = shapefile
    # shapesDF = gpd.read_file('shapefiles/World_FAO_Zones.shp')

    # converts linestring shapes to polygons for .within comparison on points
    # for i in range(len(shapesDF)):
    #     shapesDF.loc[i, 'geometry'] = shapesDF.loc[i, 'geometry'].envelope

    # declare empty variable for dataframe, switch to append to dataframe after it is created
    df=[]
    newData=True
    dfCount = 0

    # loop through files in test_data/ folder
    for file in uncutFiles:
        # create and log temporary files
        fileSplit('test_data/%s' %file)
        cutFiles = os.listdir('tabular_data/')
        # get month and year to add as df column
        monthYear = file.split('_')
        monthYear[1] = monthYear[1][:4]
        #process temporary files into dataframe
        addData = processFile(cutFiles, shapesDF)
        # empty lists for month and year columns to append to df
        addMonth = []
        addYear = []
        #fill lists with month and year equal to length of df to append
        for i in range(len(addData)):
            addMonth.append(monthYear[0])
            addYear.append(monthYear[1])
        #append columns to df
        addData['Month'] = addMonth
        addData['Year'] = addYear
        dfCount += len(addData)
        #checks to either create df or append data to df
        if newData:
            df = addData
            newData = False
            print('New df from {} with {} lines'.format(file, len(addData)))
        else: 
            df = df.append(addData, ignore_index = True)
            print('Added to df from {} with {} lines'.format(file, len(addData)))
    print('Done!')
    return df
            
def linefit(x, a, b, c, d, e, f):
    return (a * x) + (b * x**2) + (c * x**3) + (d * x**4) + (e * x**5) + f

def evaluatePolynomial(x, intercept, coefficients):
    answer = intercept
    for i in range(len(coefficients)):
        answer += (coefficients[i] * (x ** i))
    return answer

def bestRegression(X, y, degree):
    rSquare = 0
    bestDegree = 1
    bestIntercept = 0
    bestCoefficients = []
    for i in range(degree):
        poly = PolynomialFeatures(degree = (i+1))
        X_poly = poly.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_poly, y)
        linreg = LinearRegression().fit(X_train, y_train)
        if linreg.score(X_test, y_test) > rSquare:
            rSquare = linreg.score(X_test, y_test)
            bestIntercept = linreg.intercept_
            bestCoefficients = linreg.coef_
            bestDegree = (i+1)
            continue
    poly = PolynomialFeatures(bestDegree)
    X_poly = poly.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y)
    linreg = LinearRegression().fit(X_train, y_train)
    return [bestDegree, rSquare, bestIntercept, bestCoefficients]

def addZone(df, shapesDF):
    for i in range(len(shapesDF)):
        shape = shapesDF.iloc[i, :]
        for j in range(len(df)):
            point = df.iloc[j, :]
            if point.geometry.within(shape.geometry):
                df.iloc[j, 3] = shape['zone']
    return df