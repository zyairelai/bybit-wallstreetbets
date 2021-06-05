import EMA
import api_bybit
import config_bybit
from datetime import datetime
from termcolor import colored
HOUR_OR_DAY = "HOUR"

def lets_make_some_money(i):
    print(api_bybit.pair[i])
    if   HOUR_OR_DAY == "HOUR": klines = api_bybit.KLINE_INTERVAL_1HOUR(i)
    elif HOUR_OR_DAY == "DAY" : klines = api_bybit.KLINE_INTERVAL_1DAY(i)
    response = api_bybit.position_information(i)
    dataset  = api_bybit.closing_price_list(klines)
    EMA_low  = EMA.compute(3, dataset)
    EMA_high = EMA.compute(7, dataset)

    leverage = config_bybit.leverage
    if response[0].get('leverage') != leverage: api_bybit.change_leverage(i, leverage)
    if response[1].get('leverage') != leverage: api_bybit.change_leverage(i, leverage)
    if not response[0].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i, leverage)
    if not response[1].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i, leverage)

    if api_bybit.LONG_SIDE(response) == "LONGING":
        if EMA.GOING_DOWN(EMA_low):
            api_bybit.close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    if api_bybit.SHORT_SIDE(response) == "SHORTING":
        if EMA.GOING_UP(EMA_low):
            api_bybit.close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    if api_bybit.LONG_SIDE(response) == "NO_POSITION":
        if EMA.UP_TREND(EMA_low, EMA_high) and EMA.GOING_UP(EMA_low) and EMA.GOING_UP(EMA_high):
            api_bybit.open_long_position(i)
            print(colored("🚀 GO_LONG 🚀", "green"))
        else: print("🐺 WAIT 🐺")

    if api_bybit.SHORT_SIDE(response) == "NO_POSITION":
        if EMA.DOWN_TREND(EMA_low, EMA_high) and EMA.GOING_DOWN(EMA_low) and EMA.GOING_DOWN(EMA_high):
            api_bybit.open_short_position(i)
            print(colored("💥 GO_SHORT 💥", "red"))
        else: print("🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
