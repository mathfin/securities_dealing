import matplotlib.pyplot as plt
from .stockhistory import StockHistory


class Plots:
    all_plots = dict()

    def __init__(self, security_name):
        self.security_name = security_name
        if security_name in Plots.all_plots:
            raise ValueError('Such graph already exists')
        self.fig, self.ax = plt.subplots()
        Plots.all_plots[security_name] = self

    @staticmethod
    def get_by_name(security_name):
        return Plots.all_plots.get(security_name)

    def show_price_history(self):
        security_list = StockHistory.get_by_name(self.security_name).time_value_pair
        self.ax.clear()
        self.ax.set_xticklabels([])
        self.ax.set_title(self.security_name)
        self.ax.plot(list(security_list[:, 0]), list(map(float, security_list[:, 1])))
        self.ax.legend([list(map(float, security_list[:, 1]))[-1]], loc='upper left')
        self.fig.canvas.draw()

        plt.pause(0.1)
