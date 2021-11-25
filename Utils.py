import json
import argparse
from datetime import datetime

DATE_FORMAT = '%d/%m/%Y %H:%M'


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


def readJsonFile(completeFilePath):
    try:
        jsonFile = open(completeFilePath)
        data = json.load(jsonFile)  # This is a list of lists
        jsonFile.close()
        return data
    except OSError as e:
        print(e)
        exit()
    except json.JSONDecodeError:
        print('Error! The specified input file doesn\'t contains info in json format.')
        exit()


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