import Utils
import time

if __name__ == '__main__':
    start = time.time()
    args = Utils.initializeParser()
    year = Utils.getYearFromParser(args.year)
    months = Utils.getMonthToAnalizeFromParser(args.month)
    fileNames = Utils.generateFileNames(year, months)
    for fileName in fileNames:
        taxi_trip_dataframe = Utils.readCsv(fileName, (args.month is not None))
        if taxi_trip_dataframe is not None:
            payments_type = taxi_trip_dataframe.groupby(['payment_type']).size()
            most_common_pt = payments_type.idxmax()
            less_common_pt = payments_type.idxmin()
    end = time.time()
    print("Time : ", (end-start))
    #
    # payments_statistics = pd.DataFrame({'Payment Type':[Utils.PAYMENTS_TYPE_DICTIONARY.get(index) for index in payments_type.index], 'Count':payments_type.values})
    # print(payments_statistics.hist(bins=6))
    print('Hello world')