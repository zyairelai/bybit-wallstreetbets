import EMA
import config
import bybit_api
from datetime import datetime
from termcolor import colored
HOUR_OR_DAY = "HOUR"

def lets_make_some_money(i):
    print(bybit_api.pair[i])
    if   HOUR_OR_DAY == "HOUR": klines = bybit_api.KLINE_INTERVAL_1HOUR(i)
    elif HOUR_OR_DAY == "DAY" : klines = bybit_api.KLINE_INTERVAL_1DAY(i)
    response = bybit_api.position_information(i)
    dataset  = bybit_api.closing_price_list(klines)
    EMA_low  = EMA.compute(3, dataset)
    EMA_high = EMA.compute(7, dataset)

    leverage = config.leverage
    if response[0].get('leverage') != leverage: bybit_api.change_leverage(i, leverage)
    if response[1].get('leverage') != leverage: bybit_api.change_leverage(i, leverage)
    if not response[0].get('is_isolated'): bybit_api.change_margin_to_ISOLATED(i, leverage)
    if not response[1].get('is_isolated'): bybit_api.change_margin_to_ISOLATED(i, leverage)

    if bybit_api.LONG_SIDE(response) == "LONGING":
        if EMA.GOING_DOWN(EMA_low):
            bybit_api.close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    if bybit_api.SHORT_SIDE(response) == "SHORTING":
        if EMA.GOING_UP(EMA_low):
            bybit_api.close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    if bybit_api.LONG_SIDE(response) == "NO_POSITION":
        if EMA.UP_TREND(EMA_low, EMA_high) and EMA.GOING_UP(EMA_low) and EMA.GOING_UP(EMA_high):
            bybit_api.open_long_position(i)
            print(colored("🚀 GO_LONG 🚀", "green"))
        else: print("🐺 WAIT 🐺")

    if bybit_api.SHORT_SIDE(response) == "NO_POSITION":
        if EMA.DOWN_TREND(EMA_low, EMA_high) and EMA.GOING_DOWN(EMA_low) and EMA.GOING_DOWN(EMA_high):
            bybit_api.open_short_position(i)
            print(colored("💥 GO_SHORT 💥", "red"))
        else: print("🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
