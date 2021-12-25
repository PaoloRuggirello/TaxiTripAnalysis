from threading import Thread
import Utils


"""
    This is the drawer thread.
"""
class GraphDrawer(Thread):
    output_data_path = ""

    def __init__(self, queue, fig, ax):
        Thread.__init__(self)
        self.queue = queue
        self.fig = fig
        self.ax = ax

    def run(self):
        borough, data = self.queue.get()
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
        most_common_index = max(data, key=data.get)
        less_common_index = min(data, key=data.get)

        Utils.add_labels(data, self.ax)
        most_common = {most_common_index: data[most_common_index]}
        less_common = {less_common_index: data[less_common_index]}
        del data[most_common_index]
        del data[less_common_index]

        self.ax.bar(less_common.keys(), less_common.values(), color='red')
        self.ax.bar(data.keys(), data.values())
        self.ax.bar(most_common.keys(), most_common.values(), color='green')
        self.ax.set_title(borough, fontsize=30)
        self.ax.set_xlabel('Payment types')
        self.ax.set_ylabel('Number of payments')
        self.ax.legend(['Less Common payment', 'In bound payments', 'Most common payment'])
        self.fig.savefig(f'{GraphDrawer.output_data_path}{borough}.jpg', dpi=200)
        self.queue.task_done()
