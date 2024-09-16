#!/bin/python3

import ccxt, os, pandas, requests
from datetime import datetime
from pybit.unified_trading import HTTP 

coin = "BTC"
leverage = 50
trade_qty = 0.001

exchange = ccxt.bybit()
client = HTTP(
    testnet=False,
    api_key=os.environ.get('BYBIT_KEY'),
    api_secret=os.environ.get('BYBIT_SECRET'))

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get('TELEGRAM')
    chat_id = "@futures_wolves_rise"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

pair = coin + "USDT"
candlequery = 10
ccxt_client = ccxt.bybit()
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
    heikin_ashi_df["upper"] = heikin_ashi_df.apply(upper_wick, axis=1)
    heikin_ashi_df["lower"] = heikin_ashi_df.apply(lower_wick, axis=1)
    heikin_ashi_df["body"]  = abs(heikin_ashi_df['open'] - heikin_ashi_df['close'])
    heikin_ashi_df["indecisive"] = heikin_ashi_df.apply(is_indecisive, axis=1)
    heikin_ashi_df["candle"] = heikin_ashi_df.apply(valid_candle, axis=1)

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

def position_information(pair):
    response = client.get_positions(category='linear', symbol=pair)
    position = response['result']['list'][0] if response['result']['list'] else None
    return position

def set_leverage(pair, leverage, response):
    current_leverage = int(response['leverage'])
    if current_leverage and int(current_leverage) != leverage:
        client.set_leverage(symbol=pair, category='linear', buyLeverage=str(leverage), sellLeverage=str(leverage))
        print(f"Leverage set to {leverage} for {pair}.")

def market_open_long(pair, trade_qty):
    client.place_order(category="linear", symbol=pair, side='Buy', qty=trade_qty, order_type='Market')
    print("🚀 GO_LONG 🚀")

def market_open_short(pair, trade_qty):
    client.place_order(category="linear", symbol=pair, side='Sell', qty=trade_qty, order_type='Market')
    print("💥 GO_SHORT 💥")

def market_close_long(pair):
    client.place_order(symbol=pair, side='Sell', order_type='Market', qty=0, reduce_only=True, category='linear', position_idx=0)
    print("💰 CLOSED_LONG 💰")

def market_close_short(pair):
    client.place_order(symbol=pair, side='Buy', order_type='Market', qty=0, reduce_only=True, category='linear', position_idx=0)
    print("💰 CLOSED_SHORT 💰")

def wallstreetbet(pair, leverage, trade_qty):
    response = position_information(pair)
    # print(response)

    set_leverage(pair, leverage, response)
    direction = heikin_ashi(get_klines(pair, "1d"))
    twelve_hr = heikin_ashi(get_klines(pair, "12h"))
    six_hour = heikin_ashi(get_klines(pair, "6h"))
    four_hrs = heikin_ashi(get_klines(pair, "4h"))
    two_hour = heikin_ashi(get_klines(pair, "2h"))
    one_hour = heikin_ashi(get_klines(pair, "1h"))
    decimal_place = 1
    # print(direction)

    if response['size'] == '0': # Open Long Position
        if direction['candle'].iloc[-1] == "GREEN" and direction['close'].iloc[-1] > direction['close'].iloc[-2] and \
            twelve_hr['candle'].iloc[-1] == "GREEN" and \
                twelve_hr['close'].iloc[-1] > twelve_hr['close'].iloc[-2] and twelve_hr['close'].iloc[-1] > twelve_hr['close'].iloc[-3] and \
                twelve_hr['body'].iloc[-1] > twelve_hr['body'].iloc[-2] and twelve_hr['body'].iloc[-1] > twelve_hr['body'].iloc[-3] and \
            six_hour['candle'].iloc[-1] == "GREEN" and \
                six_hour['close'].iloc[-1] > six_hour['close'].iloc[-2] and six_hour['close'].iloc[-1] > six_hour['close'].iloc[-3] and \
                six_hour['body'].iloc[-1] > six_hour['body'].iloc[-2] and six_hour['body'].iloc[-1] > six_hour['body'].iloc[-3] and \
            four_hrs['candle'].iloc[-1] == "GREEN" and four_hrs['close'].iloc[-1] > four_hrs['close'].iloc[-2] and four_hrs['body'].iloc[-1] > four_hrs['body'].iloc[-2] and \
            two_hour['candle'].iloc[-1] == "GREEN" and two_hour['close'].iloc[-1] > two_hour['close'].iloc[-2] and two_hour['body'].iloc[-1] > two_hour['body'].iloc[-2] and \
            one_hour['candle'].iloc[-1] == "GREEN" and one_hour['close'].iloc[-1] > one_hour['close'].iloc[-2] and one_hour['body'].iloc[-1] > one_hour['body'].iloc[-2]:
            market_open_long(pair, trade_qty)
            telegram_bot_sendtext("BYBIT" + str(coin) + " 🚀 LONG 🚀 at " + str(round(float(response.get("markPrice")), decimal_place)))

        if direction['candle'].iloc[-1] == "RED" and direction['close'].iloc[-1] < direction['close'].iloc[-2] and \
            twelve_hr['candle'].iloc[-1] == "RED" and \
                twelve_hr['close'].iloc[-1] < twelve_hr['close'].iloc[-2] and twelve_hr['close'].iloc[-1] < twelve_hr['close'].iloc[-3] and \
                twelve_hr['body'].iloc[-1] > twelve_hr['body'].iloc[-2] and twelve_hr['body'].iloc[-1] > twelve_hr['body'].iloc[-3] and \
            six_hour['candle'].iloc[-1] == "RED" and \
                six_hour['close'].iloc[-1] < six_hour['close'].iloc[-2] and six_hour['close'].iloc[-1] < six_hour['close'].iloc[-3] and \
                six_hour['body'].iloc[-1] > six_hour['body'].iloc[-2] and six_hour['body'].iloc[-1] > six_hour['body'].iloc[-3] and \
            four_hrs['candle'].iloc[-1] == "RED" and four_hrs['close'].iloc[-1] < four_hrs['close'].iloc[-2] and four_hrs['body'].iloc[-1] > four_hrs['body'].iloc[-2] and \
            two_hour['candle'].iloc[-1] == "RED" and two_hour['close'].iloc[-1] < two_hour['close'].iloc[-2] and two_hour['body'].iloc[-1] > two_hour['body'].iloc[-2] and \
            one_hour['candle'].iloc[-1] == "RED" and one_hour['close'].iloc[-1] < one_hour['close'].iloc[-2] and one_hour['body'].iloc[-1] > one_hour['body'].iloc[-2]:
            market_open_short(pair, trade_qty)
            telegram_bot_sendtext("BYBIT" + str(coin) + " 💥 SHORT 💥 at " + str(round(float(response.get("markPrice")), decimal_place)))

    else:
        if response['size'] > '0':
            if direction['candle'].iloc[-1] != "GREEN" or twelve_hr['candle'].iloc[-1] != "GREEN" or six_hour['candle'].iloc[-1] != "GREEN" or \
                four_hrs['candle'].iloc[-1] != "GREEN" or two_hour['candle'].iloc[-1] != "GREEN" or one_hour['candle'].iloc[-1] != "GREEN":
                market_close_long()
        elif response['size'] < '0':
            if direction['candle'].iloc[-1] != "RED" or twelve_hr['candle'].iloc[-1] != "RED" or six_hour['candle'].iloc[-1] != "RED" or \
                four_hrs['candle'].iloc[-1] != "RED" or two_hour['candle'].iloc[-1] != "RED" or one_hour['candle'].iloc[-1] != "RED":
                market_close_short()
        else:
            print("YOU FUCKED UP")
    
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# Let's Get Rich
wallstreetbet(pair, leverage, trade_qty)
