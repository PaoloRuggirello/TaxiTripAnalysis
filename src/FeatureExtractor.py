import os
from threading import Thread
import pandas as pd


class FeatureExtractor(Thread):
    source_data_path = None
    year_data_path = None

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    @staticmethod
    def read_csv(file_name, raise_exception, result):
        """
            @file_name: the name of the file that should be read
            @raise_exception: if true means that the file must be present, otherwise throw and exception
            @result: used to communicate error during execution
        """
        try:
            yellow_taxi_tripdata = pd.read_csv(f'{FeatureExtractor.source_data_path}/{FeatureExtractor.year_data_path}'
                                               f'/{file_name}', usecols=['payment_type', 'DOLocationID'])
            lookup_table = pd.read_csv(f'{FeatureExtractor.source_data_path}/taxi+_zone_lookup.csv',
                                       usecols=['LocationID', 'Borough'])
            return pd.merge(yellow_taxi_tripdata, lookup_table, left_on='DOLocationID', right_on='LocationID'), file_name
        except Exception as e:
            if raise_exception:
                print(f'Data-source not found for given dates. Error message: {e}')
                result.error_during_execution()
                os._exit
            else:
                return None, None

    def run(self):
        """
            The run is used to perform the analysis.
        """
        file_name, borough, raise_exception, result = self.queue.get()
        taxi_trip_dataframe, file_name = self.read_csv(file_name, raise_exception, result)
        if taxi_trip_dataframe is not None:
            if borough is not None:  # Keeps only the borough specified by user
                taxi_trip_dataframe = taxi_trip_dataframe[taxi_trip_dataframe['Borough'] == borough]
            boroughs = taxi_trip_dataframe.groupby(['Borough'])
            for key, group in boroughs:
                payments_type = group.groupby(['payment_type']).size()
                result.fill_results(payments_type, key)
            result.add_file_name(file_name)
        self.queue.task_done()
