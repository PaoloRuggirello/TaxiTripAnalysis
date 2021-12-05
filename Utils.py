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


def initialize_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("year",
                        help="The year of which you wants to obtain the analysis",
                        type=str)
    parser.add_argument("-m", "--months",
                        help="The months of which you wants to obtain the analysis. Months must be expressed as list"
                             " of number or in english.",
                        type=str,
                        nargs='+')
    # 1+ months can be passed
    parser.add_argument("-b", "--borough",
                        help="The zone of which you wants to obtain the analysis",
                        type=str)
    parser.add_argument("-i", "--input",
                        help="The input directory where .csv files are stored",
                        default='./source-data',
                        type=str)
    parser.add_argument("-o", "--output",
                        help="The output directory where .json files and graphs will be stored.",
                        default='./output-data',
                        type=str)
    return parser.parse_args()


def get_today():
    now = datetime.now()
    return now.strftime("%d-%m-%Y %H:%M")


def get_year_from_parser(year):
    try:
        return datetime.strptime(year, '%Y').year
    except Exception as e:
        print(f'Error! Bad format for \'year\' parameter. Error message: {e}')
        exit()


def generate_file_names(year, months):
    return ['yellow_tripdata_' + str(year).zfill(4) + '-' + str(m).zfill(2) + '.csv' for m in months]


def generate_report_dir(output_path):
    os.makedirs(f'{output_path}/report ' + get_today(), exist_ok=True)


def get_month_to_analyze_from_parser(months):
    if months is not None:
        try:
            return [extract_month_num(month) for month in months]
        except Exception as e:
            print(f'Error! Month format not recognized. Error message: {e}')
            exit()
    return list(range(1, 13))


def extract_month_num(month):
    string_size = len(month)
    if string_size < 3:
        month = datetime.strptime(month, '%m').month
    elif string_size == 3:
        month = datetime.strptime(month, '%b').month
    else:
        month = datetime.strptime(month, '%B').month
    return month


def save_json_file(file_name, dump_data, indent=3):
    try:
        file = open(file_name, 'w')
        json.dump(dump_data, file, indent=indent)
        file.close()
    except OSError as e:
        print(e)
        exit()


def add_labels(dictionary):
    i = 0
    for label in dictionary:
        plt.text(i, dictionary[label], dictionary[label], ha='center')
        i += 1


def generate_graph(dest_path, borough, data):
    plt.figure(figsize=[8, 8])
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
    plt.legend(['Less Common payment', 'In bound payments', 'Most common payment'])
    plt.savefig(dest_path + borough + '.jpg', dpi=200)
