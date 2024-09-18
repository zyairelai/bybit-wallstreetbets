#!/bin/python3

import ccxt, os
from datetime import datetime
from pybit.unified_trading import HTTP 

live_trade = True
pair = "BTC" + "USDT"
trade_qty = 0.001

exchange = ccxt.bybit()
client = HTTP(
    testnet=False,
    api_key=os.environ.get('BYBIT_KEY'),
    api_secret=os.environ.get('BYBIT_SECRET'))

def position_information(pair):
    response = client.get_positions(category='linear', symbol=pair)
    position = response['result']['list'][0] if response['result']['list'] else None
    return position

def market_open_long(pair, trade_qty):
    if live_trade: client.place_order(category="linear", symbol=pair, side='Buy', qty=trade_qty, order_type='Market')
    print("🚀 GO_LONG 🚀")

def market_open_short(pair, trade_qty):
    if live_trade: client.place_order(category="linear", symbol=pair, side='Sell', qty=trade_qty, order_type='Market')
    print("💥 GO_SHORT 💥")

def market_close_long(pair):
    if live_trade: client.place_order(symbol=pair, side='Sell', order_type='Market', qty=0, reduce_only=True, category='linear', position_idx=0)
    print("💰 CLOSED_LONG 💰")

def market_close_short(pair):
    if live_trade: client.place_order(symbol=pair, side='Buy', order_type='Market', qty=0, reduce_only=True, category='linear', position_idx=0)
    print("💰 CLOSED_SHORT 💰")

def close_position(pair):
    response = position_information(pair)
    # print(response)

    if response['size'] > '0': market_close_long(pair)
    elif response['size'] < '0': market_close_short(pair)
    else: print("No position opened")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

close_position(pair)
