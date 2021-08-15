import os, time, bybit, bybit_api, EMA, math

# Get environment variables
api_key    = os.environ.get('BYBIT_KEY')
api_secret = os.environ.get('BYBIT_SECRET')
client     = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

pair = "ADA" + "USDT"
quantity = 1
price = 0.3

def get_timestamp(recent) : return int(time.time()) - recent
def KLINE_INTERVAL_1HOUR(): return client.LinearKline.LinearKline_get(symbol=pair, interval="60", limit=20, **{'from':get_timestamp(20*60*60)}).result()[0].get('result')
def KLINE_INTERVAL_1DAY() : return client.LinearKline.LinearKline_get(symbol=pair, interval="D" , limit=20, **{'from':get_timestamp(20*24*60*60)}).result()[0].get('result')
def current_close(klines): return float(klines[-1].get('close'))
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

klines = KLINE_INTERVAL_1DAY()
dataset  = bybit_api.closing_price_list(klines)
low  = EMA.compute(8, dataset)
mid  = EMA.compute(13, dataset)
high = EMA.compute(21, dataset)

number = str(56.4325)
decimal_place = number[::-1].find('.')
print(decimal_place)