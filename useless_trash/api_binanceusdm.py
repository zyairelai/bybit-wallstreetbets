import os, time, config
from binance.client import Client
from termcolor import colored

# Get environment variables
api_key     = os.environ.get('BINANCE_KEY')
api_secret  = os.environ.get('BINANCE_SECRET')
client      = Client(api_key, api_secret)
live_trade  = config.live_trade

def get_timestamp()              : return int(time.time() * 1000)
def change_leverage(i)           : return client.futures_change_leverage(symbol=config.pair[i], leverage=config.leverage[i], timestamp=get_timestamp())
def change_margin_to_ISOLATED(i) : return client.futures_change_margin_type(symbol=config.pair[i], marginType="ISOLATED", timestamp=get_timestamp())
def position_information(i)      : return client.futures_position_information(symbol=config.pair[i], timestamp=get_timestamp())[0]

def open_position(i, position, amount):
    if position == "LONG":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="MARKET", quantity=amount, timestamp=get_timestamp())
        print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
    if position == "SHORT":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="MARKET", quantity=amount, timestamp=get_timestamp())
        print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

def close_position(i,position):
    positionAmt = float(position_information(i).get('positionAmt'))
    if position == "LONG":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="SELL", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())
        print("ACTION           :   💰 CLOSE_LONG 💰")
    if position == "SHORT":
        if live_trade: client.futures_create_order(symbol=config.pair[i], side="BUY", type="MARKET", quantity=abs(positionAmt), timestamp=get_timestamp())
        print("ACTION           :   💰 CLOSE_SHORT 💰")
