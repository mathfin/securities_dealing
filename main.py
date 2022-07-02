import asyncio

from broker_connector import StockHistory, Plots, TOKEN, df, create_dict

from tinkoff.invest import (
    AsyncClient,
    LastPriceInstrument,
    MarketDataRequest,
    SubscribeLastPriceRequest,
    SubscriptionAction
)


async def main():
    for stock in list(df['name']):
        Plots(stock)               # creates an empty chart for each stock

    async def request_iterator():
        instruments = [LastPriceInstrument(figi=fg) for fg in list(df['figi'])]
        yield MarketDataRequest(
            subscribe_last_price_request=SubscribeLastPriceRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=instruments
            )
        )
        while True:
            await asyncio.sleep(1)

    async with AsyncClient(TOKEN) as client:

        async for marketdata in client.market_data_stream.market_data_stream(request_iterator()):
            market_info = create_dict(marketdata.last_price)
            print(market_info)

            if market_info is not None:
                name, time, price = market_info

                if StockHistory.all_stocks.get(name) is not None:
                    StockHistory.all_stocks.get(name).price_update([time, price])
                else:
                    StockHistory(name, [time, price])

                try:
                    Plots.get_by_name(name).show_price_history()
                except TypeError:
                    continue

            else:
                continue


if __name__ == "__main__":
    asyncio.run(main())