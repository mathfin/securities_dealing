import asyncio

from threading import Thread
from flask import Flask, render_template, url_for, request, redirect, session
from dash_application import create_dash_application
from broker_connector import StockHistory, TOKEN, df, create_dict

from tinkoff.invest import (
    AsyncClient,
    TradeInstrument,
    MarketDataRequest,
    SubscribeTradesRequest,
    SubscriptionAction
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'
create_dash_application(app)


@app.route('/', methods=["POST", "GET"])
def build_plot():
    if request.method == "POST":
        StockHistory.security_to_show = request.form['securities'].split(',')
        StockHistory.sec_to_show = int(request.form['seconds'])
        return redirect(url_for('/dash/'))
    return render_template('index.html')


async def main():

    async def request_iterator():
        instruments = [TradeInstrument(figi=fg) for fg in list(df['figi'])]
        yield MarketDataRequest(
            subscribe_trades_request=SubscribeTradesRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=instruments
            )
        )
        while True:
            await asyncio.sleep(0.1)

    async with AsyncClient(TOKEN) as client:

        async for marketdata in client.market_data_stream.market_data_stream(request_iterator()):
            market_info = create_dict(marketdata.trade)
            if market_info is not None:
                name, time, price, quantity = market_info
                if StockHistory.get_by_name(name) is not None:
                    StockHistory.get_by_name(name).price_update([time, price, quantity])
                else:
                    StockHistory(name, [time, price, quantity])

            else:
                continue


def async_main_wrapper():
    asyncio.run(main())


if __name__ == "__main__":
    th = Thread(target=async_main_wrapper)
    th.start()
    app.run(debug=False)
    th.join()

