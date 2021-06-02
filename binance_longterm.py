import config
import binance_futures_api
from termcolor import colored
from datetime import datetime

live_trade = config.live_trade
lower_EMA  = config.lower_EMA
higher_EMA = config.higher_EMA

def get_closing_price_list(klines):
    closing_price_list = []
    for candle in range(len(klines)):
        closing_price_list.append(float(klines[candle][4]))
    return closing_price_list

def calculating_EMA(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def current_EMA(EMA_list): return EMA_list[-1]
def previous_EMA(EMA_list):return EMA_list[-2]

def lets_make_some_money():
    response = binance_futures_api.position_information()[0]
    position_Amt = binance_futures_api.get_position_amount()
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR()
    
    leverage = config.leverage
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED()

    dataset = get_closing_price_list(klines_1HOUR)
    low_EMA_list  = calculating_EMA(lower_EMA, dataset)
    high_EMA_list = calculating_EMA(higher_EMA, dataset)

    current_ema_low   = current_EMA(low_EMA_list)
    current_ema_high  = current_EMA(high_EMA_list)

    if position_Amt > 0:
        if current_ema_low < current_ema_high:
            if live_trade: binance_futures_api.close_long()
            print("ACTION           :   💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_Amt < 0:
        if current_ema_low > current_ema_high:
            if live_trade: binance_futures_api.close_short()
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if current_ema_low > current_ema_high:
            if live_trade: binance_futures_api.open_long_position()
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif current_ema_low < current_ema_high:
            if live_trade: binance_futures_api.open_short_position()
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
