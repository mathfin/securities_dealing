import numpy as np
from datetime import datetime, timedelta


class StockHistory:
    all_stocks = dict()
    sec_to_show = 50  # int(input("Seconds to display on the graph: "))
    security_to_show = ['GAZP']

    def __init__(self, name, *time_value_pair):
        self.name = name
        if name in StockHistory.all_stocks:
            raise ValueError('Such graph already exists')
        self.time_value_pair = time_value_pair
        StockHistory.all_stocks[name] = self

    @staticmethod
    def get_by_name(name):
        return StockHistory.all_stocks.get(name)

    def price_update(self, *timestamp_price):
        self.time_value_pair = np.concatenate((self.time_value_pair, timestamp_price), 0)
        i = 0
        while (datetime.strptime(self.time_value_pair[-1, 0].split('.')[0], '%Y-%m-%d %H:%M:%S')
               - datetime.strptime(self.time_value_pair[i, 0].split('.')[0], '%Y-%m-%d %H:%M:%S')) \
                >= timedelta(seconds=StockHistory.sec_to_show):
            i += 1
        self.time_value_pair = self.time_value_pair[i:, :]
