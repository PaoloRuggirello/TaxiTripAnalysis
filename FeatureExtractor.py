from threading import Thread
import pandas as pd


class FeatureExtractor(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue


    def readCsv(self, fileName, raiseException):
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
        fileName, raiseException = self.queue.get()
        taxi_trip_dataframe = self.readCsv(fileName, raiseException)
        if taxi_trip_dataframe is not None:
            payments_type = taxi_trip_dataframe.groupby(['payment_type']).size()
            most_common_pt = payments_type.idxmax()
            less_common_pt = payments_type.idxmin()
        self.queue.task_done()

