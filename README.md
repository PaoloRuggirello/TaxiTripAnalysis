# **Taxi trips analyzer**
This code let's perform an analysis on taxi trips dataset based on given exercise.
Code written by:
###### PR, SPC


### Project Structure
output-data -> contains the report's result.\
source-data -> contains file used to obtain the report.\
main.py -> contains the main script to execute

### Before execution
You can download source files from: https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page \
Put dataset and lookup tables inside the source-data folder!
Otherwise, if you have source-files in another directory you can specify the path with -i option. \
The files must be collected based on the year in subdirectories. Each subdirectory has to be named with the year expressed
with the format YYYY. \
#### Example of structure: 
source-data: \
| &nbsp;&nbsp; taxi+_zone_lookup.csv \
| &nbsp;&nbsp; 2020: \
| &nbsp;&nbsp; | &nbsp;&nbsp; yellow_tripdata_2020-09.csv \
| &nbsp;&nbsp; | &nbsp;&nbsp; yellow_tripdata_2020-10.csv \
| &nbsp;&nbsp; 2021: \
| &nbsp;&nbsp; | &nbsp;&nbsp; yellow_tripdata_2020-01.csv \
| &nbsp;&nbsp; | &nbsp;&nbsp; yellow_tripdata_2020-02.csv \
######This structure must be exist also in the custom path specified with -i otion 

### Execution
To execute the script the [year] field is mandatory.\
Examples of execution commands: \
&nbsp; -This command perform the analysis to whole specified year including all boroughs. \
&nbsp;&nbsp;&nbsp;&nbsp;python3 main.py 2020 \
&nbsp; -This command perform the analysis to the specified year, with specified months including all boroughs. \
&nbsp;&nbsp;&nbsp;&nbsp;python3 main.py 2020 -m 3 6 8 \
&nbsp;&nbsp;&nbsp;&nbsp;or \
&nbsp;&nbsp;&nbsp;&nbsp;python3 main.py 2020 -m mar apr jun







