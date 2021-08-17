import os, candlestick, bybit, bybit_api, EMA

# Get environment variables
api_key    = os.environ.get('BYBIT_KEY')
api_secret = os.environ.get('BYBIT_SECRET')
client     = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

pair = "btc".upper() + "USDT"
quantity = 1
price = 0.3

def KLINE_INTERVAL_1HOUR(): return client.LinearKline.LinearKline_get(symbol=pair, interval="60", limit=20, **{'from':bybit_api.get_timestamp(20*60*60)}).result()[0].get('result')
def KLINE_INTERVAL_1DAY() : return client.LinearKline.LinearKline_get(symbol=pair, interval="D" , limit=20, **{'from':bybit_api.get_timestamp(20*24*60*60)}).result()[0].get('result')

klines = KLINE_INTERVAL_1DAY()
dataset = candlestick.closing_price_list(klines)
decimal = candlestick.price_decimal_place(klines)

low  = EMA.compute(8, dataset, decimal)
mid  = EMA.compute(13, dataset, decimal)
high = EMA.compute(21, dataset, decimal)

orderbook = client.Market.Market_orderbook(symbol=pair).result()[0].get('result')[0].get('price')

print(orderbook)

def cancle_all_active_order(): client.LinearOrder.LinearOrder_cancelAll(symbol=pair)

def limit_open_long(price):
    client.LinearOrder.LinearOrder_new(symbol=pair, side="Buy", qty=quantity, order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)

def limit_open_short(price):
    client.LinearOrder.LinearOrder_new(symbol=pair, side="Sell", qty=quantity, order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)

def limit_close_long(response, price):
    positionAmt = response[0].get('size')
    client.LinearOrder.LinearOrder_new(symbol=pair, side="Sell", qty=positionAmt, order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)

def limit_close_short(response, price):
    positionAmt = response[1].get('size')
    client.LinearOrder.LinearOrder_new(symbol=pair, side="Buy", qty=positionAmt, order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)

