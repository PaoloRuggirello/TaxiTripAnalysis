from threading import Thread
import pandas as pd


class FeatureExtractor(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def read_csv(self, fileName, raiseException):
        try:
            yellow_taxi_tripdata = pd.read_csv('source-data/' + fileName, usecols=['payment_type', 'DOLocationID'])
            lookup_table = pd.read_csv('source-data/taxi+_zone_lookup.csv', usecols=['LocationID',
                                                                                     'Borough'])  # TODO: manage possible dynamic file location and name
            return pd.merge(yellow_taxi_tripdata, lookup_table, left_on='DOLocationID', right_on='LocationID')
        except:
            if raiseException:
                print('Data-source not found for given dates.')
                exit()
            else:
                return None

    def run(self):
        fileName, borough, raiseException, result = self.queue.get()
        taxi_trip_dataframe = self.read_csv(fileName, raiseException)
        if taxi_trip_dataframe is not None:
            if borough is not None:
                taxi_trip_dataframe = taxi_trip_dataframe[taxi_trip_dataframe['Borough'] == borough]
            boroughs = taxi_trip_dataframe.groupby(['Borough'])
            for key, group in boroughs:
                payments_type = group.groupby(['payment_type']).size()
                result.fill_results(payments_type, key)
        self.queue.task_done()

