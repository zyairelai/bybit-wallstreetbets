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

def current_low(klines)  : return float(klines[-1].get('low'))

pair, leverage = [], []
for i in range(len(config.coin)):
    pair.append(config.coin[i].upper() + "USDT")
    leverage.append(config.set_Defaut_Leverage(float(client.LinearKline.LinearKline_get(symbol=pair[i], interval="1", limit=1, **{'from':get_timestamp(60)}).result()[0].get('result')[-1].get('close'))))

query = 20
def KLINE_INTERVAL_1HOUR(i): return client.LinearKline.LinearKline_get(symbol=pair[i], interval="60", limit=query, **{'from':get_timestamp(query*60*60)}).result()[0].get('result')
def KLINE_INTERVAL_1DAY(i) : return client.LinearKline.LinearKline_get(symbol=pair[i], interval="D" , limit=query, **{'from':get_timestamp(query*24*60*60)}).result()[0].get('result')
def position_information(i): return client.LinearPositions.LinearPositions_myPosition(symbol=pair[i]).result()[0].get('result')#[0_or_1].get('symbol')

def LONG_SIDE(response):
    if response[0].get('size') > 0: return "LONGING"
    elif response[0].get('size') == 0: return "NO_POSITION"

def SHORT_SIDE(response):
    if response[1].get('size') > 0 : return "SHORTING"
    elif response[1].get('size') == 0: return "NO_POSITION"

def cancle_all_active_order(i):
    if live_trade: client.LinearOrder.LinearOrder_cancelAll(symbol=pair[i])

def change_leverage(i, leverage):
    if live_trade:
        client.LinearPositions.LinearPositions_saveLeverage(symbol=pair[i], buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_ISOLATED(i, leverage):
    if live_trade:
        client.LinearPositions.LinearPositions_switchIsolated(symbol=pair[i],is_isolated=True, buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_CROSSED(i, leverage):
    if live_trade:
        client.LinearPositions.LinearPositions_switchIsolated(symbol=pair[i],is_isolated=False, buy_leverage=leverage, sell_leverage=leverage).result()

def disable_auto_add_margin(i):
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=pair[i], side="Buy", auto_add_margin=False).result()
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=pair[i], side="Sell", auto_add_margin=False).result()

def open_long_position(i):
    if live_trade: client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=config.quantity[i], order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False)

def open_short_position(i):
    if live_trade: client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=config.quantity[i], order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False)

def close_long(i, response):
    if live_trade:
        positionAmt = response[0].get('size')
        client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=positionAmt, order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()

def close_short(i, response):
    if live_trade:
        positionAmt = response[1].get('size')
        return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=positionAmt, order_type="Market", time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()

# ==================================================================================================================================================================================================================================
# LIMIT ORDER
# ==================================================================================================================================================================================================================================

def limit_open_long(i, price):
    if live_trade: client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=config.quantity[i], order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)

def limit_open_short(i, price):
    if live_trade: client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=config.quantity[i], order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)

def limit_close_long(i, response, price):
    if live_trade:
        positionAmt = response[0].get('size')
        client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=positionAmt, order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)

def limit_close_short(i, response, price):
    if live_trade:
        positionAmt = response[1].get('size')
        client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=positionAmt, order_type="Limit", price=price, time_in_force="GoodTillCancel", reduce_only=False, close_on_trigger=False)
