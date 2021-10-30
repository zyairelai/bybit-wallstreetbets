import os
import time
import config
from binance.client import Client
from termcolor import colored

# Get environment variables
api_key     = os.environ.get('BINANCE_KEY')
api_secret  = os.environ.get('BINANCE_SECRET')
client      = Client(api_key, api_secret)
live_trade  = config.live_trade

def get_timestamp():
    return int(time.time() * 1000)

def position_information(i):
    return client.futures_position_information(symbol=config.pair[i], timestamp=get_timestamp())

def LONG_SIDE(response):
    if float(response[1].get('positionAmt')) > 0: return "LONGING"
    elif float(response[2].get('positionAmt')) == 0: return "NO_POSITION"

def SHORT_SIDE(response):
    if float(response[1].get('positionAmt')) > 0 : return "SHORTING"
    elif float(response[2].get('positionAmt')) == 0: return "NO_POSITION"

def change_leverage(i):
    return client.futures_change_leverage(symbol=config.pair[i], leverage=config.leverage[i], timestamp=get_timestamp())

def change_margin_to_ISOLATED(i):
    return client.futures_change_margin_type(symbol=config.pair[i], marginType="ISOLATED", timestamp=get_timestamp())

def set_one_way_mode():
    if client.futures_get_position_mode(timestamp=get_timestamp()).get('dualSidePosition'):
        return client.futures_change_position_mode(dualSidePosition="false", timestamp=get_timestamp())

def set_hedge_mode(): 
    if not client.futures_get_position_mode(timestamp=get_timestamp()).get('dualSidePosition'):
        return client.futures_change_position_mode(dualSidePosition="true", timestamp=get_timestamp())

def market_open_long(i):
    if live_trade:
        client.futures_create_order(symbol=config.pair[i],
                                    quantity=config.quantity[i],
                                    positionSide="LONG",
                                    type="MARKET",
                                    side="BUY",
                                    timestamp=get_timestamp())
    print(colored("🚀 GO_LONG 🚀", "green"))

def market_open_short(i):
    if live_trade:
        client.futures_create_order(symbol=config.pair[i],
                                    quantity=config.quantity[i],
                                    positionSide="SHORT",
                                    type="MARKET",
                                    side="SELL",
                                    timestamp=get_timestamp())
    print(colored("💥 GO_SHORT 💥", "red"))

def market_close_long(i, response):
    if live_trade:
        client.futures_create_order(symbol=config.pair[i],
                                    quantity=abs(float(response[1].get('positionAmt'))),
                                    positionSide="LONG",
                                    side="SELL",
                                    type="MARKET",
                                    timestamp=get_timestamp())
    print("💰 CLOSE_LONG 💰")

def market_close_short(i, response):
    if live_trade:
        client.futures_create_order(symbol=config.pair[i],
                                    quantity=abs(float(response[2].get('positionAmt'))),
                                    positionSide="SHORT",
                                    side="BUY",
                                    type="MARKET",
                                    timestamp=get_timestamp())
    print("💰 CLOSE_SHORT 💰")

set_hedge_mode()