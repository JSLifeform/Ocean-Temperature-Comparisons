# Ocean Temperatures from Wrold Oceanic Database

This project is designed to measure oceanic temperature changes from the years 1987 to 2015. It is designed to run in Jupyter Notebook. Any data to be tested is in the test_data/ folder. The project was written with Python version 3.7.10 and conda version 4.9.2. The necessary dependencies are listed in the requirements.txt file. 

### Recommended install procedure

1.) download the project folder from GitHub. 

2.) Open the Anaconda Prompt.

3.) Navigate to the project folder in the Anaconda prompt.

4.) Create a new environment with the command: conda create --name Geoviews 

Using "--file requirements.txt" on the above command to create the environment seems to cause issues with Geoviews. You can try it if you like, but if the ocean heat maps do not show up you will have to install the dependencies manually. The below lines manually install the necessary dependencies:

conda install Geoviews
conda install Seaborn
conda install geopandas
pip install sklearn

5.) Activate the new environment with the command: conda activate Geoviews (or GeoviewsManual if used)

6.) open Jupyter Notebook with command: Jupyter Notebook

7.) Once Notebook is opened, open the OceanTemps.ipynb file and run all cells.

NOTE: It may take several minutes to run


