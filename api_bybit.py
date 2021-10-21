import os
import time
import bybit
import config

# Get environment variables
api_key    = os.environ.get('BYBIT_KEY')
api_secret = os.environ.get('BYBIT_SECRET')
client     = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)
live_trade = config.live_trade

def get_timestamp(recent):
    return int(time.time()) - recent

def position_information(i):
    return client.LinearPositions.LinearPositions_myPosition(symbol=config.pair[i]).result()[0].get('result')#[0_or_1].get('symbol')

def LONG_SIDE(response):
    if response[0].get('size') > 0: return "LONGING"
    elif response[0].get('size') == 0: return "NO_POSITION"

def SHORT_SIDE(response):
    if response[1].get('size') > 0 : return "SHORTING"
    elif response[1].get('size') == 0: return "NO_POSITION"

def change_leverage(i):
    if live_trade: client.LinearPositions.LinearPositions_saveLeverage(symbol=config.pair[i], buy_leverage=config.leverage[i], sell_leverage=config.leverage[i]).result()

def change_margin_to_ISOLATED(i):
    if live_trade: client.LinearPositions.LinearPositions_switchIsolated(symbol=config.pair[i],is_isolated=True, buy_leverage=config.leverage[i], sell_leverage=config.leverage[i]).result()

def change_margin_to_CROSSED(i):
    if live_trade: client.LinearPositions.LinearPositions_switchIsolated(symbol=config.pair[i],is_isolated=False, buy_leverage=config.leverage[i], sell_leverage=config.leverage[i]).result()

def disable_auto_add_margin(i):
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=config.pair[i], side="Buy", auto_add_margin=False).result()
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=config.pair[i], side="Sell", auto_add_margin=False).result()

def market_open_long(i):
    if live_trade: client.LinearOrder.LinearOrder_new(symbol=config.pair[i], side="Buy", qty=config.quantity[i], order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False).result()

def market_open_short(i):
    if live_trade: client.LinearOrder.LinearOrder_new(symbol=config.pair[i], side="Sell", qty=config.quantity[i], order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False).result()

def market_close_long(i, response):
    if live_trade:
        positionAmt = response[0].get('size')
        client.LinearOrder.LinearOrder_new(symbol=config.pair[i], side="Sell", qty=positionAmt, order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()

def market_close_short(i, response):
    if live_trade:
        positionAmt = response[1].get('size')
        client.LinearOrder.LinearOrder_new(symbol=config.pair[i], side="Buy", qty=positionAmt, order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()
