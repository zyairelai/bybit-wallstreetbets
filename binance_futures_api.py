import os, time, config_binance
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

pair = []
for i in range(len(config_binance.coin)):
    pair.append(config_binance.coin[i] + "USDT")

def get_timestamp():
    return int(time.time() * 1000)

def KLINE_INTERVAL_1HOUR(i):
    return client.futures_klines(symbol=pair[i], limit=100, interval=Client.KLINE_INTERVAL_1HOUR)

def KLINE_INTERVAL_1DAY(i):
    return client.futures_klines(symbol=pair[i], limit=100, interval=Client.KLINE_INTERVAL_1DAY)

def position_information(i):
    return client.futures_position_information(symbol=pair[i], timestamp=get_timestamp())

def get_position_amount(i):
    return float(position_information(i)[0].get('positionAmt'))

def change_leverage(i, leverage):
    client.futures_change_leverage(symbol=pair[i], leverage=leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED(i):
    client.futures_change_margin_type(symbol=pair[i], marginType="ISOLATED", timestamp=get_timestamp())

def change_margin_to_CROSSED(i):
    client.futures_change_margin_type(symbol=pair[i], marginType="CROSSED", timestamp=get_timestamp())

def open_long_position(i):
    client.futures_create_order(symbol=pair[i], side="BUY", type="MARKET", quantity=config_binance.quantity[i], timestamp=get_timestamp())

def open_short_position(i):
    client.futures_create_order(symbol=pair[i], side="SELL", type="MARKET", quantity=config_binance.quantity[i], timestamp=get_timestamp())

def close_long(i):
    positionAmt = abs(get_position_amount(i))
    client.futures_create_order(symbol=pair[i], side="SELL", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())

def close_short(i):
    positionAmt = abs(get_position_amount(i))
    client.futures_create_order(symbol=pair[i], side="BUY", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())

def get_closing_price_list(klines):
    closing_price_list = []
    for candle in range(len(klines)):
        closing_price_list.append(float(klines[candle][4]))
    return closing_price_list
