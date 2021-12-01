import matplotlib.pyplot as plt
import pandas as pd

import Utils

if __name__ == '__main__':
    args = Utils.initializeParser()
    year = Utils.getYearFromParser(args.year)
    month = Utils.getMonthFromParser(args.month)
    fileName = Utils.generateFileName(year, month)
    taxi_trip_dataframe = Utils.readCsv(fileName)
    payments_type = taxi_trip_dataframe.groupby(['payment_type']).size()
    most_common_pt = payments_type.idxmax()
    less_common_pt = payments_type.idxmin()
    print(Utils.PAYMENTS_TYPE_DICTIONARY.get(most_common_pt))
    print(Utils.PAYMENTS_TYPE_DICTIONARY.get(less_common_pt))
    #
    # payments_statistics = pd.DataFrame({'Payment Type':[Utils.PAYMENTS_TYPE_DICTIONARY.get(index) for index in payments_type.index], 'Count':payments_type.values})
    # print(payments_statistics.hist(bins=6))
    print('Hello world')