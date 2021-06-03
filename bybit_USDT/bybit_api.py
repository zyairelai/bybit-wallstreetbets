import os
import time
import bybit
import config

# Get environment variables
api_key    = os.environ.get('BYBIT_API')
api_secret = os.environ.get('BYBIT_SECRET')
client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

def get_timestamp():
    return int(time.time()) - 2592000

def get_klines(i):
    return client.LinearKline.LinearKline_get(symbol=config.pair[i], interval="D", limit=50, **{'from':get_timestamp()}).result()[0].get('result')

def closing_price_list(klines):
    closing_price_list = []
    for count in range(len(klines)):
        closing_price_list.append(klines[count].get('close'))
    return closing_price_list

def position_information(i):
    return client.LinearPositions.LinearPositions_myPosition(symbol=config.pair[i]).result()[0].get('result')[0]#.get('symbol')


"""
def get_position_amount(i):
    return float(position_information(i)[0].get('positionAmt'))
"""

def change_leverage(i, leverage):
    client.LinearPositions.LinearPositions_saveLeverage(symbol=config.pair[i], buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_ISOLATED(i, leverage):
    client.LinearPositions.LinearPositions_switchIsolated(symbol=config.pair[i],is_isolated=True, buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_CROSSED(i, leverage):
    client.LinearPositions.LinearPositions_switchIsolated(symbol=config.pair[i],is_isolated=False, buy_leverage=leverage, sell_leverage=leverage).result()

def disable_auto_add_margin(i):
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=config.pair[i], side="Buy", auto_add_margin=False).result()
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=config.pair[i], side="Sell", auto_add_margin=False).result()

"""
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
"""
