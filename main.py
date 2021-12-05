import time
import Utils
from queue import Queue
from FeatureExtractor import FeatureExtractor
from Result import Result


def start_feature_extractors():
    queue = Queue()
    for fileName in fileNames:
        extractor = FeatureExtractor(queue)
        extractor.start()
        queue.put((fileName, args.borough, args.month is not None, result))
    queue.join()


def generate_graphs():
    for borough in result.result:
        Utils.generate_graph(reportPath, borough, result.result[borough])


if __name__ == '__main__':
    start = time.time()

    args = Utils.initialize_parser()
    year = Utils.get_year_from_parser(args.year)
    # TODO manage list of months
    months = Utils.get_month_to_analyze_from_parser(args.month)
    fileNames = Utils.generate_file_names(year, months)

    result = Result()
    start_feature_extractors()

    Utils.generate_report_dir()
    reportPath = 'output-data/report ' + Utils.get_today() + '/'
    Utils.save_json_file(reportPath + 'result.json', result.result)
    generate_graphs()

    end = time.time()
    print("Execution time : ", (end-start))
    print("You can find the generated report here: " + reportPath)