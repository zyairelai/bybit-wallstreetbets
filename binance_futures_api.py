import os
import time
import config
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('BINANCE_KEY')
api_secret  = os.environ.get('BINANCE_SECRET')
client      = Client(api_key, api_secret)
live_trade  = config.live_trade

query = 20
pair = []

for i in range(len(config.coin)) : pair.append(config.coin[i] + "USDT")
def KLINE_INTERVAL_5MINUTE(i)    : return client.futures_klines(symbol=pair[i], limit=query, interval=Client.KLINE_INTERVAL_5MINUTE)
def KLINE_INTERVAL_15MINUTE(i)   : return client.futures_klines(symbol=pair[i], limit=query, interval=Client.KLINE_INTERVAL_15MINUTE)
def KLINE_INTERVAL_1HOUR(i)      : return client.futures_klines(symbol=pair[i], limit=query, interval=Client.KLINE_INTERVAL_1HOUR)
def KLINE_INTERVAL_4HOUR(i)      : return client.futures_klines(symbol=pair[i], limit=query, interval=Client.KLINE_INTERVAL_4HOUR)
def KLINE_INTERVAL_1DAY(i)       : return client.futures_klines(symbol=pair[i], limit=query, interval=Client.KLINE_INTERVAL_1DAY)
def account_trades(i, timestamp) : return client.futures_account_trades(symbol=pair[i], timestamp=get_timestamp(), startTime=timestamp)
def position_information(i)      : return client.futures_position_information(symbol=pair[i], timestamp=get_timestamp())[0]
def get_position_amount(i)       : return float(position_information(i).get('positionAmt'))

def get_timestamp():
    return int(time.time() * 1000)

def closing_price_list(klines):
    closing_price_list = []
    for candle in range(len(klines)):
        closing_price_list.append(float(klines[candle][4]))
    return closing_price_list

def change_leverage(i, leverage):
    if live_trade:
        client.futures_change_leverage(symbol=pair[i], leverage=leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED(i):
    if live_trade:
        client.futures_change_margin_type(symbol=pair[i], marginType="ISOLATED", timestamp=get_timestamp())

def change_margin_to_CROSSED(i):
    if live_trade:
        client.futures_change_margin_type(symbol=pair[i], marginType="CROSSED", timestamp=get_timestamp())

def open_long_position(i):
    if live_trade:
        client.futures_create_order(symbol=pair[i], side="BUY", type="MARKET", quantity=config.quantity[i], timestamp=get_timestamp())

def open_short_position(i):
    if live_trade:
        client.futures_create_order(symbol=pair[i], side="SELL", type="MARKET", quantity=config.quantity[i], timestamp=get_timestamp())

def close_long(i, response):
    if live_trade:
        positionAmt = abs(float(response.get('positionAmt')))
        client.futures_create_order(symbol=pair[i], side="SELL", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())

def close_short(i, response):
    if live_trade:
        positionAmt = abs(float(response.get('positionAmt')))
        client.futures_create_order(symbol=pair[i], side="BUY", type="MARKET", quantity=positionAmt, timestamp=get_timestamp())

def current_open(klines)  : return float(klines[-1][1])
def current_high(klines)  : return float(klines[-1][2])
def current_low(klines)   : return float(klines[-1][3])
def current_close(klines) : return float(klines[-1][4])
def candle_body(klines)   : return abs(current_open(klines) - current_close(klines))
def candle_wick(klines)   : return current_high(klines) - current_low(klines) - candle_body(klines)

def candle_color(klines):
    if current_close(klines) > current_open(klines): return "GREEN"
    elif current_close(klines) < current_open(klines): return "RED"
    else: return "INDECISIVE"

def upper_wick(klines):
    if candle_color(klines) == "GREEN": return current_high(klines) - current_close(klines)
    elif candle_color(klines) == "RED": return current_high(klines) - current_open(klines)
    else: return 0

def lower_wick(klines):
    if candle_color(klines) == "GREEN": return current_open(klines)  - current_low(klines)
    elif candle_color(klines) == "RED": return current_close(klines) - current_low(klines)
    else: return 0

def strong_candle(klines):
    if candle_body(klines) > candle_wick(klines): return True
