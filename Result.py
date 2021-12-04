from Utils import PAYMENTS_TYPE_DICTIONARY as payment_type


class Result:

    def __init__(self):
        self.result = {}

    def get_borough(self, borough):
        if borough not in self.result:
            self.result[borough] = {}
        return self.result[borough]

    def fill_results(self, threadResults, borough):
        for threadResult in threadResults.iteritems():
            boroughResult = self.get_borough(borough)
            if payment_type[threadResult[0]] in boroughResult:
                boroughResult[payment_type[threadResult[0]]] = boroughResult[payment_type[threadResult[0]]] + threadResult[1]
            else:
                boroughResult[payment_type[threadResult[0]]] = threadResult[1]
