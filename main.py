import Utils
import time
from queue import Queue
from FeatureExtractor import FeatureExtractor
from Result import Result


def startFeatureExtractors():
    queue = Queue()
    for fileName in fileNames:
        extractor = FeatureExtractor(queue)
        extractor.start()
        queue.put((fileName, args.borough, args.month is not None, result))
    queue.join()


if __name__ == '__main__':
    start = time.time()
    args = Utils.initializeParser()
    year = Utils.getYearFromParser(args.year)
    months = Utils.getMonthToAnalyzeFromParser(args.month)
    fileNames = Utils.generateFileNames(year, months)
    result = Result()
    startFeatureExtractors()

    # print('Most common: ', max(result.result, key=result.result.get))
    # print('Less common: ', min(result.result, key=result.result.get))
    print(result.result)
    end = time.time()
    print("Time : ", (end-start))
    #
    # payments_statistics = pd.DataFrame({'Payment Type':[Utils.PAYMENTS_TYPE_DICTIONARY.get(index) for index in payments_type.index], 'Count':payments_type.values})
    # print(payments_statistics.hist(bins=6))
    print('Hello world')