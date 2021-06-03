import EMA
import api_bybit
import config_bybit
from datetime import datetime
from termcolor import colored

lower_EMA  = 3
higher_EMA = 7
live_trade = config_bybit.live_trade

def lets_make_some_money(i):
    klines = api_bybit.get_klines(i)
    dataset = api_bybit.closing_price_list(klines)
    response = api_bybit.position_information(i)

    low_EMA_list  = EMA.compute(lower_EMA, dataset)
    high_EMA_list = EMA.compute(higher_EMA, dataset)
    current_ema_low  = EMA.current(low_EMA_list)
    current_ema_high = EMA.current(high_EMA_list)

    if live_trade: # Initial Setup
        leverage = config_bybit.leverage
        if response[0].get('leverage') != leverage: api_bybit.change_leverage(i, leverage)
        if response[1].get('leverage') != leverage: api_bybit.change_leverage(i, leverage)
        if not response[0].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i, leverage)
        if not response[1].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i, leverage)

    print(api_bybit.pair[i])

    if EMA.GOING_UP(current_ema_low, current_ema_high):
        if live_trade:
            if api_bybit.LONG_SIDE(response) == "NO_POSITION": api_bybit.open_long_position(i)
            if api_bybit.SHORT_SIDE(response) == "SHORTING": api_bybit.close_short(i)
        print(colored("🚀 TO_THE_MOON 🚀", "green"))

    elif EMA.GOING_DOWN(current_ema_low, current_ema_high):
        if live_trade:
            if api_bybit.SHORT_SIDE(response) == "NO_POSITION": api_bybit.open_short_position(i)
            if api_bybit.LONG_SIDE(response)  == "LONGING": api_bybit.close_long(i)
        print(colored("💥 TO_THE_MARS 💥", "red"))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
