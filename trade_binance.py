import EMA
import config_binance
import api_binance_futures
from datetime import datetime
from termcolor import colored
HOUR_OR_DAY = "HOUR"

def lets_make_some_money(i):
    print(api_binance_futures.pair[i])
    if   HOUR_OR_DAY == "HOUR": klines = api_binance_futures.KLINE_INTERVAL_1HOUR(i)
    elif HOUR_OR_DAY == "DAY" : klines = api_binance_futures.KLINE_INTERVAL_1DAY(i)
    response = api_binance_futures.position_information(i)[0]
    dataset  = api_binance_futures.closing_price_list(klines)
    EMA_low  = EMA.compute(3, dataset)
    EMA_high = EMA.compute(7, dataset)

    leverage = config_binance.leverage
    if int(response.get("leverage")) != leverage: api_binance_futures.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": api_binance_futures.change_margin_to_ISOLATED(i)

    if api_binance_futures.get_position_amount(i) > 0: # LONGING
        if EMA.GOING_DOWN(EMA_low):
            api_binance_futures.close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("HOLDING_LONG", "green"))

    elif api_binance_futures.get_position_amount(i) < 0: # SHORTING
        if EMA.GOING_UP(EMA_low):
            api_binance_futures.close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("HOLDING_SHORT", "red"))

    else:
        if EMA.UP_TREND(EMA_low, EMA_high) and EMA.GOING_UP(EMA_low) and EMA.GOING_UP(EMA_high):
            api_binance_futures.open_long_position(i)
            print(colored("🚀 GO_LONG 🚀", "green"))

        elif EMA.DOWN_TREND(EMA_low, EMA_high) and EMA.GOING_DOWN(EMA_low) and EMA.GOING_DOWN(EMA_high):
            api_binance_futures.open_short_position(i)
            print(colored("💥 GO_SHORT 💥", "red"))

        else: print("🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
