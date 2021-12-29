from src.Utils import PAYMENTS_TYPE_DICTIONARY as PAYMENT_TYPE
from threading import Lock


class Result:
    """
    This class is used to join results from threads.
    """

    def __init__(self):
        self.result = {}
        self.lock_extraction = Lock()
        self.lock_file_names = Lock()
        self.error_during_thread_execution = False
        self.file_names_analyzed = []

    def get_borough(self, borough):
        if borough not in self.result:
            self.result[borough] = {}
        return self.result[borough]

    def error_during_execution(self):
        self.error_during_thread_execution = True

    def fill_results(self, thread_results, borough):
        if not self.error_during_thread_execution:  # Save result only if execution is ok
            self.lock_extraction.acquire()  # Lock is needed to obtain a consistent result
            for thread_result in thread_results.iteritems():
                borough_result = self.get_borough(borough)
                if PAYMENT_TYPE[thread_result[0]] in borough_result:
                    borough_result[PAYMENT_TYPE[thread_result[0]]] += thread_result[1]
                else:
                    borough_result[PAYMENT_TYPE[thread_result[0]]] = thread_result[1]
            self.lock_extraction.release()
    
    def add_file_name(self, file_name):
        if not self.error_during_thread_execution:
            self.lock_file_names.acquire()
            self.file_names_analyzed.append(file_name)
            self.lock_file_names.release()
            