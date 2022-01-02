import json
import argparse
from datetime import datetime
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
    return now.strftime("%d-%m-%Y_%H:%M")


def get_year_from_parser(year):
    try:
        return datetime.strptime(year, '%Y').year
    except Exception as e:
        print(f'Error! Bad format for \'year\' parameter. Error message: {e}')
        exit()


def generate_file_names(year, months):
    return ['yellow_tripdata_' + str(year).zfill(4) + '-' + str(m).zfill(2) + '.csv' for m in months]


def generate_report_dir(output_path):
    report_output_path = f'{output_path}/report_' + get_today()
    subdir_output_path = f'{report_output_path}/graphs'
    # creating main output dir and graphs subdir
    os.makedirs(f'{subdir_output_path}', exist_ok=True)
    return report_output_path, subdir_output_path


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
    if string_size < 3:  # Convert numbers in month
        month = datetime.strptime(month, '%m').month
    elif string_size == 3:  # Convert small string in numbers es. jan, feb, mar ecc.
        month = datetime.strptime(month, '%b').month
    else:  # Convert string to month es january, february, march ecc.
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


def save_text_file(file_name, lines):
    try:
        file = open(file_name, 'w')
        file.writelines(lines)
        file.close()
    except OSError as e:
        print(e)
        exit()


def add_labels(dictionary, ax):
    """
        This method set the number of payments up to the corresponding payment method.
    """
    i = 0
    for label in dictionary:
        ax.text(i, dictionary[label], dictionary[label], ha='center')
        i += 1


def get_summary_of_analysis(args, year_got, file_names_analyzed, analyzed_boroughs, start, end) -> list:
    """
        This method returns a list of text rows that summarizes the analysis done
    """
    return [
        'PARAMETERS INSERTED BY USER\n',
        f'Input_directory: {args.input}\n',
        f'Output_directory: {args.output}\n',
        f"Boroughs' info: {args.input}/taxi+_zone_lookup.csv\n",
        f'Year: {args.year}\n',
        f"Months: {args.months if args.months is not None else 'all'}\n",
        f"Borough: {args.borough if args.borough is not None else 'all'}\n\n\n",
        'ACTUAL ANALYSIS WAS PERFORMED ON\n'
        f'Taxi data subdirectory: {args.input}/{year_got}/\n',
        f"Files analyzed: {file_names_analyzed}\n",
        f"Boroughs analyzed: {analyzed_boroughs}\n\n\n"
        'METRICS OF ANALYSIS\n',
        f'Start datetime: {datetime.fromtimestamp(start)}\n',
        f'End datetime: {datetime.fromtimestamp(end)}\n',
        f"Execution time : {end - start} s"
    ]
