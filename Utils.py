import json
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import os

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
                        help="The month of which you wants to obtain the analysis. Month must be expressed as number "
                             "or in english.",
                        type=str)
    parser.add_argument("-b", "--borough",
                        help="The zone of which you wants to obtain the analysis",
                        type=str)
    return parser.parse_args()


def saveJsonFile(filePath, dumpData, indent=3):
    try:
        file = open(filePath, 'w')
        json.dump(dumpData, file, indent=indent)
        file.close()
    except OSError as e:
        print(e)
        exit()


def getToday():
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M")


def getYearFromParser(year):
    try:
        return datetime.strptime(year, '%Y').year
    except:
        print('Error! Bad format for \'year\' parameter.')
        exit()


def generateFileNames(year, months):
    return ['yellow_tripdata_' + str(year).zfill(4) + '-' + str(m).zfill(2) + '.csv' for m in months]


def generateReportDir():
    try:
        os.mkdir('output-data/report ' + getToday())
    except FileExistsError:
        print('INFO - Given folder already exists')


def getMonthToAnalyzeFromParser(month):
    if month is not None:
        try:
            stringSize = len(month)
            if stringSize < 3:
                month = datetime.strptime(month, '%m').month
            elif stringSize == 3:
                month = datetime.strptime(month, '%b').month
            else:
                month = datetime.strptime(month, '%B').month
            return [month]
        except:
            print('Error! Month format not recognized.')
            exit()
    return list(range(1, 13))


def saveJsonFile(fileName, dumpData, indent=3):
    try:
        file = open(fileName, 'w')
        json.dump(dumpData, file, indent=indent)
        file.close()
    except OSError as e:
        print(e)
        exit()


def add_labels(dictionary):
    i = 0
    for label in dictionary:
        plt.text(i, dictionary[label], dictionary[label], ha = 'center')
        i += 1


def generateGraph(destPath, borough, data):
    plt.figure(figsize=[10, 10])
    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
    most_common_index = max(data, key=data.get)
    less_common_index = min(data, key=data.get)

    add_labels(data)
    most_common = {most_common_index: data[most_common_index]}
    less_common = {less_common_index: data[less_common_index]}
    del data[most_common_index]
    del data[less_common_index]

    plt.bar(less_common.keys(), less_common.values(), color='red')
    plt.bar(data.keys(), data.values())
    plt.bar(most_common.keys(), most_common.values(), color='green')
    plt.title(borough, fontsize=30)
    plt.xlabel('Payment types')
    plt.ylabel('Number of payments')
    plt.legend(['In bound payments', 'Most common payment', 'Less Common payment'])
    plt.savefig(destPath + borough + '.jpg', dpi=300)
    return plt
