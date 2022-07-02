import pandas as pd

from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService
from .token_file import TOKEN


rts = input("Companies ticker to show:").split(",")


with Client(TOKEN) as cl:
    instruments: InstrumentsService = cl.instruments
    ticker_to_figi_list = []

    for item in getattr(instruments, 'shares')().instruments:
        if item.ticker in rts:
            ticker_to_figi_list.append({
                'ticker': item.ticker,
                'figi': item.figi,
                'name': item.name
            })

df = pd.DataFrame(ticker_to_figi_list)
print(df)
