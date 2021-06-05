import EMA
import config
import binance_futures_api
from datetime import datetime
from termcolor import colored
HOUR_OR_DAY = "HOUR"

def lets_make_some_money(i):
    print(binance_futures_api.pair[i])
    if   HOUR_OR_DAY == "HOUR": klines = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    elif HOUR_OR_DAY == "DAY" : klines = binance_futures_api.KLINE_INTERVAL_1DAY(i)
    response = binance_futures_api.position_information(i)[0]
    dataset  = binance_futures_api.closing_price_list(klines)
    EMA_low  = EMA.compute(3, dataset)
    EMA_high = EMA.compute(7, dataset)

    leverage = config.leverage
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if binance_futures_api.get_position_amount(i) > 0: # LONGING
        if EMA.GOING_DOWN(EMA_low):
            binance_futures_api.close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("HOLDING_LONG", "green"))

    elif binance_futures_api.get_position_amount(i) < 0: # SHORTING
        if EMA.GOING_UP(EMA_low):
            binance_futures_api.close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("HOLDING_SHORT", "red"))

    else:
        if EMA.UP_TREND(EMA_low, EMA_high) and EMA.GOING_UP(EMA_low) and EMA.GOING_UP(EMA_high):
            binance_futures_api.open_long_position(i)
            print(colored("🚀 GO_LONG 🚀", "green"))

        elif EMA.DOWN_TREND(EMA_low, EMA_high) and EMA.GOING_DOWN(EMA_low) and EMA.GOING_DOWN(EMA_high):
            binance_futures_api.open_short_position(i)
            print(colored("💥 GO_SHORT 💥", "red"))

        else: print("🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
