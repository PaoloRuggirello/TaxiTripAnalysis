import time
import Utils
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

    end = time.time()
    Utils.generateReportDir()
    reportPath = 'output-data/report ' + Utils.getToday() + '/'
    Utils.saveJsonFile(reportPath + 'result.json', result.result)
    for borough in result.result:
        plt = Utils.generateGraph(reportPath, borough, result.result[borough])
    print("Execution time : ", (end-start))
    print("You can find the generated report here: " + reportPath)