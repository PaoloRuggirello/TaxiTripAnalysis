import Utils
import time
from queue import Queue
from FeatureExtractor import FeatureExtractor

if __name__ == '__main__':
    start = time.time()
    args = Utils.initializeParser()
    year = Utils.getYearFromParser(args.year)
    months = Utils.getMonthToAnalyzeFromParser(args.month)
    fileNames = Utils.generateFileNames(year, months)
    queue = Queue()
    for fileName in fileNames:
        extractor = FeatureExtractor(queue)
        extractor.start()
        queue.put((fileName, args.month is not None))
    queue.join()
    end = time.time()
    print("Time : ", (end-start))
    #
    # payments_statistics = pd.DataFrame({'Payment Type':[Utils.PAYMENTS_TYPE_DICTIONARY.get(index) for index in payments_type.index], 'Count':payments_type.values})
    # print(payments_statistics.hist(bins=6))
    print('Hello world')