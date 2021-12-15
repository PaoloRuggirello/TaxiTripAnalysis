import datetime
import time
import Utils
import matplotlib.pyplot as plt
from queue import Queue
from FeatureExtractor import FeatureExtractor
from GraphDrawer import GraphDrawer
from Result import Result


def start_feature_extractors(source_data):
    queue_extractor = Queue()
    FeatureExtractor.source_data_path = source_data
    for fileName in fileNames:
        extractor = FeatureExtractor(queue_extractor)
        extractor.start()
        queue_extractor.put((fileName, args.borough, args.months is not None, result))
    queue_extractor.join()


def generate_graphs(output_path):
    queue_graphs = Queue()
    GraphDrawer.output_data_path = output_path
    for borough in result.result:
        # .subplots permits to draw graphs using threads
        fig, ax = plt.subplots()
        drawer = GraphDrawer(queue_graphs, fig, ax)
        drawer.start()
        queue_graphs.put((borough, result.result[borough]))
    queue_graphs.join()


if __name__ == '__main__':
    start = time.time()
    print(f"Starting TaxiTripAnalysis at: {datetime.datetime.fromtimestamp(start)}\n")

    args = Utils.initialize_parser()
    print(f"Input data dir: {args.input}\n")
    year = Utils.get_year_from_parser(args.year)
    months = Utils.get_month_to_analyze_from_parser(args.months)
    print(f"Analysing data of year: {year} | months: {months} ...\n")
    fileNames = Utils.generate_file_names(year, months)

    result = Result()
    start_feature_extractors(args.input)

    reportPath, graphPath = Utils.generate_report_dir(args.output)
    Utils.save_json_file(f'{reportPath}/result.json', result.result)
    generate_graphs(f'{graphPath}/')

    end = time.time()
    print(f"Ended TaxiTripAnalysis at: {datetime.datetime.fromtimestamp(end)}")
    print(f"Execution time : {end-start} s\n")
    print(f"You can find the generated report here: {reportPath}")
    print(f"and graphs in the subdirectory: {graphPath}")
