import os, time, config
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

query = 100

def KLINE_INTERVAL_1HOUR(i):
    return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_1HOUR)

def KLINE_INTERVAL_1DAY(i):
    return client.futures_klines(symbol=config.pair[i], limit=query, interval=Client.KLINE_INTERVAL_1DAY)

def position_information(i):
    return client.futures_position_information(symbol=config.pair[i], timestamp=get_timestamp())

def get_position_amount(i):
    return float(position_information(i)[0].get('positionAmt'))

def change_leverage(i, leverage):
    return client.futures_change_leverage(symbol=config.pair[i], leverage=leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED(i):
    return client.futures_change_margin_type(symbol=config.pair[i], marginType="ISOLATED", timestamp=get_timestamp())

def change_margin_to_CROSSED(i):
    return client.futures_change_margin_type(symbol=config.pair[i], marginType="CROSSED", timestamp=get_timestamp())

def open_long_position(i):
    client.futures_create_order(symbol=config.pair[i], side="BUY", type="MARKET", quantity=config.quantity[i], timestamp=get_timestamp())

def open_short_position(i):
    client.futures_create_order(symbol=config.pair[i], side="SELL", type="MARKET", quantity=config.quantity[i], timestamp=get_timestamp())

def close_long(i):
    positionAmt = abs(get_position_amount(i))
    client.futures_create_order(symbol=config.pair[i], side="SELL", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())

def close_short(i):
    positionAmt = abs(get_position_amount(i))
    client.futures_create_order(symbol=config.pair[i], side="BUY", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())
