from .ticker_to_figi import df


def create_dict(c):
    try:
        name = list(df.loc[(df['figi'] == c.figi)]['name'])[0]
        time = str(c.time)
        price = float(cast_money(c.price))
        quantity = int(c.quantity)
        return name, time, price, quantity

    except AttributeError:
        return None


def cast_money(v):

    return v.units + v.nano / 1e9