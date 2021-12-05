from threading import Thread
import matplotlib.pyplot as plt
import Utils


class GraphDrawer(Thread):
    output_data_path = ""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        borough, data = self.queue.get()
        # .subplots permits to draw graphs using threads
        fig, ax = plt.subplots()
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
        most_common_index = max(data, key=data.get)
        less_common_index = min(data, key=data.get)

        Utils.add_labels(data, ax)
        most_common = {most_common_index: data[most_common_index]}
        less_common = {less_common_index: data[less_common_index]}
        del data[most_common_index]
        del data[less_common_index]

        ax.bar(less_common.keys(), less_common.values(), color='red')
        ax.bar(data.keys(), data.values())
        ax.bar(most_common.keys(), most_common.values(), color='green')
        ax.set_title(borough, fontsize=30)
        ax.set_xlabel('Payment types')
        ax.set_ylabel('Number of payments')
        ax.legend(['Less Common payment', 'In bound payments', 'Most common payment'])
        fig.savefig(f'{GraphDrawer.output_data_path}{borough}.jpg', dpi=200)
        self.queue.task_done()
