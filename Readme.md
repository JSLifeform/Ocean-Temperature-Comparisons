# Ocean Temperatures from World Oceanic Database

This project is designed to measure oceanic temperature changes from the years 1987 to 2015. It is designed to run in Jupyter Notebook. Any data to be tested is in the test_data/ folder. The project was written with Python version 3.7.10 and conda version 4.9.2. The necessary dependencies are listed in the requirements.txt file. 

### Recommended install procedure

1.) download the project folder from GitHub. 

2.) Open the Anaconda Prompt.

3.) Navigate to the project folder in the Anaconda prompt.

4a.) Create a new environment with the command: conda create --name Geoviews --file requirements.txt

5a.) Activate the new environment with the command: conda activate Geoviews


Using "--file requirements.txt" on the above command to create the environment can occasionally cause issues with Geoviews. You can try it if you like, but if the ocean heat maps do not show up you may need to install the dependencies manually. This can be done by following steps 4b, 5b, and 6. You may skip step 6 if you complete the setup with 4a and 4b.

4b.) Create a new environment with the command: conda create --name GeoviewsManual

5.) Activate the new environment with the command: conda activate GeoviewsManual

6.) (WARNING: Skip this step if you set up the environment with steps 4a and 5a) The below lines manually install the necessary dependencies:

conda install -c pyviz geoviews    
pip install sklearn  


7.) open Jupyter Notebook with command: jupyter notebook

8.) Once Notebook is opened, open the OceanTemps.ipynb file.

9.) Run the top cell with the import statements.

10.) Once the top cell is finished running, you may run all below. There is a Run All Below Command under the Cell header in Jupyter Notebook.

NOTE: It may take several minutes to run


