import time
import Utils
from queue import Queue
from FeatureExtractor import FeatureExtractor
from Result import Result


def start_feature_extractors(source_data):
    queue = Queue()
    FeatureExtractor.source_data_path = source_data
    for fileName in fileNames:
        extractor = FeatureExtractor(queue)
        extractor.start()
        queue.put((fileName, args.borough, args.months is not None, result))
    queue.join()


def generate_graphs():
    for borough in result.result:
        Utils.generate_graph(reportPath, borough, result.result[borough])


if __name__ == '__main__':
    start = time.time()

    args = Utils.initialize_parser()
    year = Utils.get_year_from_parser(args.year)
    months = Utils.get_month_to_analyze_from_parser(args.months)
    fileNames = Utils.generate_file_names(year, months)

    result = Result()
    start_feature_extractors(args.input)

    Utils.generate_report_dir(args.output)
    reportPath = f'{args.output}/report {Utils.get_today()}/'
    Utils.save_json_file(f'{reportPath}result.json', result.result)
    generate_graphs()

    end = time.time()
    print("Execution time : ", (end-start))
    print(f"You can find the generated report here: {reportPath}")
