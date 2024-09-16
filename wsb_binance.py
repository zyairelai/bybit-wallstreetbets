#!/usr/bin/python3

live_trade = True

import os, time, pandas, ccxt
from binance.client import Client
from datetime import datetime

if live_trade: print("------ LIVE TRADE IS ENABLED ------\n", "green")

# Initialize Trade Size
coin = "BTC"
leverage = 50
quantity = 0.002

# Print for cnnfirmation
pair = coin + "USDT"
print("\nPair Name  : " + pair)
print("Quantity   : " + str(quantity) + " " + coin)
print("Leverage   : " + str(leverage) + "\n")

# Get environment variables
api_key    = os.environ.get('BINANCE_KEY')
api_secret = os.environ.get('BINANCE_SECRET')
client     = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

def position_information(pair):
    return client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0]

def account_trades(pair, timestamp) :
    return client.futures_account_trades(symbol=pair, timestamp=get_timestamp(), startTime=timestamp)

def LONG_SIDE(response):
    if float(response.get('positionAmt')) > 0: return "LONGING"
    elif float(response.get('positionAmt')) == 0: return "NO_POSITION"
    else: return "YOU'RE FUCKED"

def SHORT_SIDE(response):
    if float(response.get('positionAmt')) < 0 : return "SHORTING"
    elif float(response.get('positionAmt')) == 0: return "NO_POSITION"
    else: return "YOU'RE FUCKED"

def change_leverage(pair, leverage):
    if live_trade: return client.futures_change_leverage(symbol=pair, leverage=leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED(pair):
    if live_trade: return client.futures_change_margin_type(symbol=pair, marginType="ISOLATED", timestamp=get_timestamp())

def one_way_mode():
    if client.futures_get_position_mode(timestamp=get_timestamp()).get('dualSidePosition'):
        return client.futures_change_position_mode(dualSidePosition="false", timestamp=get_timestamp())

def set_hedge_mode():
    if not client.futures_get_position_mode(timestamp=get_timestamp()).get('dualSidePosition'):
        return client.futures_change_position_mode(dualSidePosition="true", timestamp=get_timestamp())

if live_trade: one_way_mode()

def market_open_long(pair, quantity):
    if live_trade:
        client.futures_create_order(symbol=pair, quantity=quantity, type="MARKET", side="BUY", timestamp=get_timestamp())
    print("🚀 GO_LONG 🚀", "green")

def market_open_short(pair, quantity):
    if live_trade:
        client.futures_create_order(symbol=pair, quantity=quantity, type="MARKET", side="SELL", timestamp=get_timestamp())
    print("💥 GO_SHORT 💥", "red")

def market_close_long(pair, response):
    if live_trade:
        client.futures_create_order(symbol=pair, quantity=abs(float(response.get('positionAmt'))), side="SELL", type="MARKET", timestamp=get_timestamp())
    print("💰 CLOSE_LONG 💰")

def market_close_short(pair, response):
    if live_trade:
        client.futures_create_order(symbol=pair, quantity=abs(float(response.get('positionAmt'))), side="BUY", type="MARKET", timestamp=get_timestamp())
    print("💰 CLOSE_SHORT 💰")

candlequery = 100
ccxt_client = ccxt.binance()
tohlcv_colume = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

def get_klines(pair, interval):
    return pandas.DataFrame(ccxt_client.fetch_ohlcv(pair, interval , limit=candlequery), columns=tohlcv_colume)

def heikin_ashi(klines):
    heikin_ashi_df = pandas.DataFrame(index=klines.index.values, columns=['open', 'high', 'low', 'close'])
    heikin_ashi_df['close'] = (klines['open'] + klines['high'] + klines['low'] + klines['close']) / 4

    for i in range(len(klines)):
        if i == 0: heikin_ashi_df.iat[0, 0] = klines['open'].iloc[0]
        else: heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(klines['high']).max(axis=1)
    heikin_ashi_df['low']  = heikin_ashi_df.loc[:, ['open', 'close']].join(klines['low']).min(axis=1)
    heikin_ashi_df["color"] = heikin_ashi_df.apply(color, axis=1)
    heikin_ashi_df.insert(0,'timestamp', klines['timestamp'])
    heikin_ashi_df["volume"] = klines["volume"]

    # Use Temporary Column to Identify Strength
    heikin_ashi_df["upper"] = heikin_ashi_df.apply(upper_wick, axis=1)
    heikin_ashi_df["lower"] = heikin_ashi_df.apply(lower_wick, axis=1)
    heikin_ashi_df["body"]  = abs(heikin_ashi_df['open'] - heikin_ashi_df['close'])
    heikin_ashi_df["indecisive"] = heikin_ashi_df.apply(is_indecisive, axis=1)
    heikin_ashi_df["candle"] = heikin_ashi_df.apply(valid_candle, axis=1)

    # Calculate body size as percentage of the range
    heikin_ashi_df['body_size'] = (heikin_ashi_df['body'] / (heikin_ashi_df['high'] - heikin_ashi_df['low'])) * 100
    return heikin_ashi_df

def color(HA):
    if   HA['open'] < HA['close']: return "GREEN"
    elif HA['open'] > HA['close']: return "RED"
    else: return "INDECISIVE"

def upper_wick(HA):
    if HA['color'] == "GREEN": return HA['high'] - HA['close']
    elif HA['color'] == "RED": return HA['high'] - HA['open']
    else: return (HA['high'] - HA['open'] + HA['high'] - HA['close']) / 2

def lower_wick(HA):
    if HA['color'] == "GREEN": return  HA['open'] - HA['low']
    elif HA['color'] == "RED": return HA['close'] - HA['low']
    else: return (HA['open'] - HA['low'] + HA['close'] - HA['low']) / 2

def is_indecisive(HA):
    if HA['upper'] > HA['body'] and HA['lower'] > HA['body']: return True
    else: return False

def valid_candle(HA):
    if not HA['indecisive']:
        if HA['color'] == "GREEN": return "GREEN"
        elif HA['color'] == "RED": return "RED"
    else: return "INDECISIVE"

def close_wallstreetbet(pair):
    response = position_information(pair)
    # print(response)
    if LONG_SIDE(response) == "LONGING": market_close_long(pair, response)
    elif SHORT_SIDE(response) == "SHORTING":market_close_short(pair, response)
    else: print("YOU FUCKED UP")

def open_wallstreetbet(pair, leverage, quantity):
    response = position_information(pair)
    # print(response)

    if response.get('marginType') != "isolated": change_margin_to_ISOLATED(pair)
    if int(response.get("leverage")) != leverage: change_leverage(pair, leverage)

    direction = heikin_ashi(get_klines(pair, "1d"))
    # print(direction)

    if LONG_SIDE(response) == "NO_POSITION": # Open Long Position
        if direction['candle'].iloc[-1] == "GREEN" and direction['body_size'].iloc[-1] > 0.5:
            market_open_long(pair, quantity)
        else: print("FUCKING INDECISIVE")

    if SHORT_SIDE(response) == "NO_POSITION": # Open Short Position
        if direction['candle'].iloc[-1] == "RED" and direction['body_size'].iloc[-1] > 0.5:
            market_open_short(pair, quantity)
        else: print("FUCKING INDECISIVE")

    if LONG_SIDE(response) == "NO_POSITION" and SHORT_SIDE(response) == "NO_POSITION":
        print("🐺 WAIT 🐺")

close_wallstreetbet(pair)
time.sleep(60)
open_wallstreetbet(pair, leverage, quantity)
print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
