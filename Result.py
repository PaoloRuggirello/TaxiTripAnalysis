from Utils import PAYMENTS_TYPE_DICTIONARY as PAYMENT_TYPE


class Result:

    def __init__(self):
        self.result = {}

    def get_borough(self, borough):
        if borough not in self.result:
            self.result[borough] = {}
        return self.result[borough]

    def fill_results(self, thread_results, borough):
        for thread_result in thread_results.iteritems():
            borough_result = self.get_borough(borough)
            if PAYMENT_TYPE[thread_result[0]] in borough_result:
                borough_result[PAYMENT_TYPE[thread_result[0]]] += thread_result[1]
            else:
                borough_result[PAYMENT_TYPE[thread_result[0]]] = thread_result[1]
