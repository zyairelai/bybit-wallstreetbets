import EMA
import bybit_api
import config_bybit
from datetime import datetime
from termcolor import colored

lower_EMA  = 3
higher_EMA = 7
live_trade = config_bybit.live_trade

def lets_make_some_money(i):
    klines = bybit_api.get_klines(i)
    dataset = bybit_api.closing_price_list(klines)
    response = bybit_api.position_information(i)

    low_EMA_list  = EMA.compute(lower_EMA, dataset)
    high_EMA_list = EMA.compute(higher_EMA, dataset)
    current_ema_low  = EMA.current(low_EMA_list)
    current_ema_high = EMA.current(high_EMA_list)

    if live_trade: # Initial Setup
        leverage = config_bybit.leverage
        if response.get('leverage') != leverage: bybit_api.change_leverage(i, leverage)
        if not response.get('is_isolated'): bybit_api.change_margin_to_ISOLATED(i, leverage)

    print(bybit_api.pair[i])
    if bybit_api.position_info(response) == "LONGING":
        if EMA.GOING_DOWN(current_ema_low, current_ema_high):
            if live_trade: bybit_api.close_long(i, response)
            print("ACTION           :   💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif bybit_api.position_info(response) == "SHORTING":
        if EMA.GOING_UP(current_ema_low, current_ema_high):
            if live_trade: bybit_api.close_short(i, response)
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if EMA.GOING_UP(current_ema_low, current_ema_high):
            if live_trade: bybit_api.open_long_position(i)
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif EMA.GOING_DOWN(current_ema_low, current_ema_high):
            if live_trade: bybit_api.open_short_position(i)
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
