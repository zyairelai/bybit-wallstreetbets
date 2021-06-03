import os, time, bybit, config_bybit

# Get environment variables
api_key    = os.environ.get('api_bybit')
api_secret = os.environ.get('BYBIT_SECRET')
client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

pair = []
for i in range(len(config_bybit.coin)):
    pair.append(config_bybit.coin[i] + "USDT")

def get_timestamp():
    return int(time.time()) - 2592000

def get_klines(i):
    return client.LinearKline.LinearKline_get(symbol=pair[i], interval="D", limit=50, **{'from':get_timestamp()}).result()[0].get('result')    

def position_information(i):
    return client.LinearPositions.LinearPositions_myPosition(symbol=pair[i]).result()[0].get('result')

def LONG_SIDE(response):
    if response[0].get('size') > 0: return "LONGING"
    elif response[0].get('size') == 0: return "NO_POSITION"

def SHORT_SIDE(response):
    if response[1].get('size') > 0 : return "SHORTING"
    elif response[1].get('size') == 0: return "NO_POSITION"

def change_leverage(i, leverage):
    client.LinearPositions.LinearPositions_saveLeverage(symbol=pair[i], buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_ISOLATED(i, leverage):
    client.LinearPositions.LinearPositions_switchIsolated(symbol=pair[i],is_isolated=True, buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_CROSSED(i, leverage):
    client.LinearPositions.LinearPositions_switchIsolated(symbol=pair[i],is_isolated=False, buy_leverage=leverage, sell_leverage=leverage).result()

def disable_auto_add_margin(i):
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=pair[i], side="Buy", auto_add_margin=False).result()
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=pair[i], side="Sell", auto_add_margin=False).result()

def open_long_position(i):
    return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=config_bybit.quantity[i], order_type="Market",
    time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False).result()

def open_short_position(i):
    return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=config_bybit.quantity[i], order_type="Market",
    time_in_force="ImmediateOrCancel",reduce_only=False, close_on_trigger=False).result()

def close_long(i, response):
    positionAmt = response[0].get('size')
    return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Sell", qty=positionAmt, order_type="Market",
    time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()

def close_short(i, response):
    positionAmt = response[1].get('size')
    return client.LinearOrder.LinearOrder_new(symbol=pair[i], side="Buy", qty=positionAmt, order_type="Market",
    time_in_force="ImmediateOrCancel",reduce_only=True, close_on_trigger=False).result()

def closing_price_list(klines):
    closing_price_list = []
    for count in range(len(klines)):
        closing_price_list.append(klines[count].get('close'))
    return closing_price_list