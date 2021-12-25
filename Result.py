from Utils import PAYMENTS_TYPE_DICTIONARY as PAYMENT_TYPE
from threading import Lock


"""
This class is used to join results from threads.
"""
class Result:

    def __init__(self):
        self.result = {}
        self.lock = Lock()

    def get_borough(self, borough):
        if borough not in self.result:
            self.result[borough] = {}
        return self.result[borough]

    def fill_results(self, thread_results, borough):
        self.lock.acquire()  # Lock is needed to obtain a consistent result
        for thread_result in thread_results.iteritems():
            borough_result = self.get_borough(borough)
            if PAYMENT_TYPE[thread_result[0]] in borough_result:
                borough_result[PAYMENT_TYPE[thread_result[0]]] += thread_result[1]
            else:
                borough_result[PAYMENT_TYPE[thread_result[0]]] = thread_result[1]
        self.lock.release()
