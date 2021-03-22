import sys
import os
import numpy as np
import re
import pandas as pd
import panel as pn
from IPython.display import display
import scipy as sc
import time
import matplotlib as plt
import geoviews as gv
import geoviews.feature as gf
import xarray as xr
from geoviews import opts
from cartopy import crs
import geopandas as gpd
import geoviews.tile_sources as gvts
from shapely import geometry
import fiona
gv.extension('bokeh')

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
    for i in range(int(180/latitude)):
        p1 = [-180, (i*latitude)-90.00000]
        p2 = [180, (i*latitude)-90.00000]
        p3 = [180, ((i+1)*latitude)-90.00000]
        p4 = [-180, ((i+1)*latitude)-90.00000]
        pointList = [p1, p2, p3, p4, p1]
        poly = geometry.Polygon(pointList)
        globeLat.loc[i] = [(i*latitude-90) , poly]
        globeLat.append({'zone': (i*latitude-90) , 'geometry': poly}, ignore_index = True)
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

    # loop through files in data/ folder
    for file in uncutFiles:
        # create and log temporary files
        fileSplit('data/%s' %file)
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
            