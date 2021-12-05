from threading import Thread
import pandas as pd


class FeatureExtractor(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    @staticmethod
    def read_csv(file_name, raise_exception):
        try:
            yellow_taxi_tripdata = pd.read_csv('source-data/' + file_name, usecols=['payment_type', 'DOLocationID'])
            # TODO: manage possible dynamic file location and name
            lookup_table = pd.read_csv('source-data/taxi+_zone_lookup.csv', usecols=['LocationID',
                                                                                     'Borough'])
            return pd.merge(yellow_taxi_tripdata, lookup_table, left_on='DOLocationID', right_on='LocationID')
        except Exception as e:
            if raise_exception:
                print(f'Data-source not found for given dates. Error message: {e}')
                exit()
            else:
                return None

    def run(self):
        file_name, borough, raise_exception, result = self.queue.get()
        taxi_trip_dataframe = self.read_csv(file_name, raise_exception)
        if taxi_trip_dataframe is not None:
            if borough is not None:
                taxi_trip_dataframe = taxi_trip_dataframe[taxi_trip_dataframe['Borough'] == borough]
            boroughs = taxi_trip_dataframe.groupby(['Borough'])
            for key, group in boroughs:
                payments_type = group.groupby(['payment_type']).size()
                result.fill_results(payments_type, key)
        self.queue.task_done()

