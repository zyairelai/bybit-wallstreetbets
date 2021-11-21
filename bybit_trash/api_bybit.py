import os
import time
import bybit
import config
from termcolor import colored

# Get environment variables
api_key    = os.environ.get('BYBIT_KEY')
api_secret = os.environ.get('BYBIT_SECRET')
client     = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)
live_trade = config.live_trade

def get_timestamp(recent):
    return int(time.time()) - recent

def position_information(pair):
    return client.LinearPositions.LinearPositions_myPosition(symbol=pair).result()[0].get('result')#[0_or_1].get('symbol')

print(position_information("BTCUSDT")[0])

def LONG_SIDE(response):
    if response[0].get('size') > 0: return "LONGING"
    elif response[0].get('size') == 0: return "NO_POSITION"

def SHORT_SIDE(response):
    if response[1].get('size') > 0 : return "SHORTING"
    elif response[1].get('size') == 0: return "NO_POSITION"

def change_leverage(pair, leverage):
    if live_trade: client.LinearPositions.LinearPositions_saveLeverage(symbol=pair, buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_ISOLATED(pair, leverage):
    if live_trade: client.LinearPositions.LinearPositions_switchIsolated(symbol=pair,is_isolated=True, buy_leverage=leverage, sell_leverage=leverage).result()

def change_margin_to_CROSSED(pair, leverage):
    if live_trade: client.LinearPositions.LinearPositions_switchIsolated(symbol=pair,is_isolated=False, buy_leverage=leverage, sell_leverage=leverage).result()

def disable_auto_add_margin(pair):
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=pair, side="Buy", auto_add_margin=False).result()
    client.LinearPositions.LinearPositions_setAutoAddMargin(symbol=pair, side="Sell", auto_add_margin=False).result()

def market_open_long(pair, quantity):
    if live_trade:
        client.LinearOrder.LinearOrder_new(symbol=pair,
                                           qty=quantity,
                                           side="Buy",
                                           order_type="Market",
                                           time_in_force="ImmediateOrCancel",
                                           reduce_only=False, 
                                           close_on_trigger=False).result()
    print(colored("🚀 GO_LONG 🚀", "green"))

def market_open_short(pair, quantity):
    if live_trade:
        client.LinearOrder.LinearOrder_new(symbol=pair,
                                           qty=quantity,
                                           side="Sell",
                                           order_type="Market",
                                           time_in_force="ImmediateOrCancel",
                                           reduce_only=False,
                                           close_on_trigger=False).result()
    print(colored("💥 GO_SHORT 💥", "red"))

def market_close_long(pair, response):
    if live_trade:
        client.LinearOrder.LinearOrder_new(symbol=pair,
                                           qty=response[0].get('size'),
                                           side="Sell",
                                           order_type="Market",
                                           time_in_force="ImmediateOrCancel",
                                           reduce_only=True,
                                           close_on_trigger=False).result()
    print("💰 CLOSE_LONG 💰")

def market_close_short(pair, response):
    if live_trade:
        client.LinearOrder.LinearOrder_new(symbol=pair,
                                           qty=response[1].get('size'),
                                           side="Buy",
                                           order_type="Market",
                                           time_in_force="ImmediateOrCancel",
                                           reduce_only=True,
                                           close_on_trigger=False).result()
    print("💰 CLOSE_SHORT 💰")

def test_trailing_stop(pair, quantity):
        client.Positions.Positions_tradingStop(symbol="BTCUSD",
                                               take_profit="0",
                                               stop_loss="9110",
                                               trailing_stop="0",
                                               new_trailing_active="0").result()