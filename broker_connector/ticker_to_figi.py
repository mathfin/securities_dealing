import pandas as pd

from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService
from .token_file import TOKEN


sec_name = ['TSLA', 'BABA', 'GAZP', 'SBER'] # input("Tickers to show:").split(",")


with Client(TOKEN) as cl:
    instruments: InstrumentsService = cl.instruments
    ticker_to_figi_list = []

    for asset_type in ['shares', 'currencies', 'bonds', 'futures']:
        for item in getattr(instruments, asset_type)().instruments:
            if item.ticker in sec_name:
                ticker_to_figi_list.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'name': item.name
                })


df = pd.DataFrame(ticker_to_figi_list)
