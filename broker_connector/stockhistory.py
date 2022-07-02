import numpy as np


class StockHistory:
    all_stocks = dict()

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