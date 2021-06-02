import os, time, config
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

query = 100

def KLINE_INTERVAL_1HOUR():
    return client.futures_klines(symbol=config.pairname, limit=query, interval=Client.KLINE_INTERVAL_1HOUR)

def position_information():
    return client.futures_position_information(symbol=config.pairname, timestamp=get_timestamp())

def get_position_amount():
    return float(position_information()[0].get('positionAmt'))

def change_leverage(leverage):
    return client.futures_change_leverage(symbol=config.pairname, leverage=leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED():
    return client.futures_change_margin_type(symbol=config.pairname, marginType="ISOLATED", timestamp=get_timestamp())

def change_margin_to_CROSSED():
    return client.futures_change_margin_type(symbol=config.pairname, marginType="CROSSED", timestamp=get_timestamp())

def open_long_position():
    client.futures_create_order(symbol=config.pairname, side="BUY", type="MARKET", quantity=config.amount, timestamp=get_timestamp())

def open_short_position():
    client.futures_create_order(symbol=config.pairname, side="SELL", type="MARKET", quantity=config.amount, timestamp=get_timestamp())

def close_long():
    positionAmt = abs(get_position_amount())
    client.futures_create_order(symbol=config.pairname, side="SELL", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())

def close_short():
    positionAmt = abs(get_position_amount())
    client.futures_create_order(symbol=config.pairname, side="BUY", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())

