# Ocean Temperatures from World Oceanic Database

This project is designed to measure oceanic temperature changes from the years 1987 to 2015. It is designed to run in Jupyter Notebook. Any data to be tested is in the test_data/ folder. The project was written with Python version 3.7.10 and conda version 4.9.2. The necessary dependencies are listed in the requirements.txt file. 

### Note to Mac users

1.) In the limited testing on Mac systems, an issue has arisen where a hidden file was added in the tabular_data\ folder which caused a UnicodeDecodeError in the second cell of the project. Further testing is necessary, but it is possible the hidden file was added when the project was downloaded/unzipped from GitHub. If a UnicodeDecodeError occurs on your run of the project, perform the following; shut down the kernel, delete the tabular_data\ folder, and recreate a new empty folder named tabular_data within the project folder.

If any experienced Mac users can shed light on what caused this hidden file to appear, any feedback to the project creator would be appreciated.

### Recommended install procedure

1.) download the project folder from GitHub. 

2.) Open the Anaconda Prompt.

3.) Navigate to the project folder in the Anaconda prompt.

Method A:

4a.) Create a new environment with the command: conda create --name Geoviews --file requirements.txt

5a.) Activate the new environment with the command: conda activate Geoviews


Using "--file requirements.txt" on the above command to create the environment can occasionally cause issues with Geoviews. You can try it if you like, but if the ocean heat maps do not show up you may need to install the dependencies manually. This can be done by following steps 4b, 5b, and 6. You may skip step 6 if you complete the setup with 4a and 4b.

Method B:

4b.) Create a new environment with the command: conda create --name GeoviewsManual

5.) Activate the new environment with the command: conda activate GeoviewsManual



6.) (WARNING: Skip this step if you set up the environment with steps Method A) The below lines manually install the necessary dependencies:

conda install -c pyviz geoviews    
pip install sklearn  


7.) open Jupyter Notebook with command: jupyter notebook

8.) Once Notebook is opened, open the OceanTemps.ipynb file.

9.) Run the top cell with the import statements.

10.) Once the top cell is finished running, you may run all below. There is a Run All Below Command under the Cell header in Jupyter Notebook.

NOTE: It may take several minutes to run. There should be 2 heat maps that show, in output cell 10 and the final output cell. If they do not run, there are a couple methods that have helped show them:

1.) Rerun the top cell, then Run all Cells Below a 2nd time

2.) close the kernel and restart, then Run All Cells

3.) Close the project and Jupyter Notebook, stop the jupyter instance running in the Conda Prompt and restart a new Conda Prompt. Use this Conda Prompt to navigate to the project folder, then use "conda activate Geoviews" followed by "jupyter notebook" and rerun the project. Past tests have shown it to work if you simply Run All Cells, but it is still recommended to run the top cell, followed by Run All Below.

4.) If method A was used to set up the environment, try creating a new environment using method B.


### Installing/Running Project Outside Conda prompt

The program was designed and tested using a conda prompt/Jupyter Notebook instance within the project folder, but it should run from any folder within your computer. It was tested using the Jupyter GUI to install packages with mixed success -  the project runs but the heat maps had issues appearing. If you use this method and the heat maps do not appear the first time, close all of Jupyter completely and restart the program, then run the project again.

This project is NOT recommended to set up via pip/pip3 install. The Geoviews dependencies do not seem to work well with a pip install, and the conda environment setup is required to install it properly and easily. If you insist on installing it via pip (especially within a Windows environment), it is strongly recommended you read [this](https://stackoverflow.com/questions/56531106/how-to-install-geoviews-in-python) and [this](https://stackoverflow.com/questions/53697814/using-pip-install-to-install-cartopy-but-missing-proj-version-at-least-4-9-0) thread from StackOverflow. Many an hour was sacrificed by this project designer for the simple desire to use pipenv over a conda environment - -I recommend you do NOT make the same mistake!

## Special Thanks

Special thanks to Code Louisville, mentors Nate Kratzer and Will Tirone, and especially my group mentor Pratik for all their help in creating this project! Another shout out to all my classmates who aided me with their own expertise, personal advice, and emotional handholding as I dug myself further into (and eventually out of) the proverbial weeds while working on this project. One final mention of gratitude towards Robert, DeVontrae, Evan, Violet, and any other mentors I've neglected to mention on this long journey towards the mastery of 1's and 0's. Peace be with all!


