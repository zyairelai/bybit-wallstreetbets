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
    pair.append(config.coin[i] + "USDT")
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

def closing_price_list(klines):
    closing_price_list = []
    for count in range(len(klines)):
        closing_price_list.append(klines[count].get('close'))
    return closing_price_list

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
    if live_trade:
        return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=config.quantity[i], order_type="Market",
        time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False).result()

def open_short_position(i):
    if live_trade:
        return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=config.quantity[i], order_type="Market",
        time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False).result()

def close_long(i, response):
    if live_trade:
        positionAmt = response[0].get('size')
        return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=positionAmt, order_type="Market",
        time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()

def close_short(i, response):
    if live_trade:
        positionAmt = response[1].get('size')
        return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=positionAmt, order_type="Market",
        time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()

def current_open(klines) : return float(klines[-1].get('open'))
def current_close(klines): return float(klines[-1].get('close'))
def current_high(klines) : return float(klines[-1].get('high'))
def current_low(klines)  : return float(klines[-1].get('low'))
def candle_body(klines)  : return abs(current_open(klines) - current_close(klines))
def candle_wick(klines)  : return current_high(klines) - current_low(klines) - candle_body(klines)

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
