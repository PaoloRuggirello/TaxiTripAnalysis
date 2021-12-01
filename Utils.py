import json
import argparse
import pandas as pd
from datetime import datetime

PAYMENTS_TYPE_DICTIONARY = {
        1: 'Credit card',
        2: 'Cash',
        3: 'No charge',
        4: 'Dispute',
        5: 'Unknown',
        6: 'Voided trip'
}


def initializeParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("year",
                        help="The year of which you wants to obtain the analysis",
                        type=str)
    parser.add_argument("-m", "--month",
                        help="The year of which you wants to obtain the analysis. Month must be expressed as number "
                             "or in english.",
                        type=str)
    parser.add_argument("-b", "--borough",
                        help="The zone of which you wants to obtain the analysis",
                        type=str,
                        default='.json')
    return parser.parse_args()


def saveJsonFile(filePath, dumpData, indent=3):
    try:
        file = open(filePath, 'w')
        json.dump(dumpData, file, indent=indent)
        file.close()
    except OSError as e:
        print(e)
        exit()


def getYearFromParser(year):
    try:
        return datetime.strptime(year, '%Y').year
    except:
        print('Error! Bad format for \'year\' parameter.')
        exit()


def generateFileName(year, month):
    return 'yellow_tripdata_' + str(year).zfill(4) + '-' + str(month).zfill(2) + '.csv'


def getMonthFromParser(month):
    if month != None:
        try:
            stringSize = len(month)
            if stringSize < 3:
                month = datetime.strptime(month, '%m').month
            elif stringSize == 3:
                month = datetime.strptime(month, '%b').month
            else:
                month = datetime.strptime(month, '%B').month
            return month
        except:
            print('Error! Month format not recognized.')
            exit()
    return month


def readCsv(fileName):
    try:
        yellow_taxi_tripdata = pd.read_csv('source-data/'+fileName, usecols=['payment_type', 'DOLocationID'])
        lookup_table = pd.read_csv('source-data/taxi+_zone_lookup.csv', usecols=['LocationID', 'Borough'])  #TODO: manage possible dynamic file location and name
        return pd.merge(yellow_taxi_tripdata, lookup_table, left_on='DOLocationID', right_on='LocationID')
    except Exception as execption:
        # print('Data-source not found for given dates.')
        print(execption)