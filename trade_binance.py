import config, EMA
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    print(binance_futures_api.pair[i])
    klines   = binance_futures_api.KLINE_INTERVAL_1DAY(i)
    response = binance_futures_api.position_information(i)
    dataset  = binance_futures_api.closing_price_list(klines)

    low  = EMA.compute(5, dataset)
    mid  = EMA.compute(8, dataset)
    high = EMA.compute(13, dataset)

    leverage = binance_futures_api.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if binance_futures_api.get_position_amount(i) > 0: # LONGING
        if EXIT_LONG_CONDITION(klines, low, mid, high):
            binance_futures_api.close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("HOLDING_LONG", "green"))

    elif binance_futures_api.get_position_amount(i) < 0: # SHORTING
        if EXIT_SHORT_CONDITION(klines, low, mid, high):
            binance_futures_api.close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("HOLDING_SHORT", "red"))

    else:
        if GO_LONG_CONDITION(klines, low, mid, high):
            binance_futures_api.open_long_position(i)
            print(colored("🚀 GO_LONG 🚀", "green"))

        elif GO_SHORT_CONDITION(klines, low, mid, high):
            binance_futures_api.open_short_position(i)
            print(colored("💥 GO_SHORT 💥", "red"))

        else: print("🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                    ENTRY CONDITIONS
# ==========================================================================================================================================================================

def GO_LONG_CONDITION(klines, low, mid, high):
    if not EMA.ABSOLUTE_DOWNTREND(low, mid, high) and EMA.DELTA_UPWARD(low, mid, high) and \
        binance_futures_api.current_close(klines) > EMA.MIDDLE(low, mid, high) and \
        binance_futures_api.strong_candle(klines) and \
        binance_futures_api.candle_color(klines) == "GREEN": return True

def GO_SHORT_CONDITION(klines, low, mid, high):
    if not EMA.ABSOLUTE_UPTREND(low, mid, high) and EMA.DELTA_DOWNWARD(low, mid, high) and \
        binance_futures_api.current_close(klines) < EMA.MIDDLE(low, mid, high) and \
        binance_futures_api.strong_candle(klines) and \
        binance_futures_api.candle_color(klines) == "RED": return True

def EXIT_LONG_CONDITION(klines, low, mid, high):
    if (binance_futures_api.candle_body(klines) > binance_futures_api.previous_candle_body(klines) or \
        binance_futures_api.current_close(klines) < EMA.HIGHEST(low, mid, high) or EMA.DOWNWARD_MOVEMENT(low)) and \
        binance_futures_api.candle_color(klines) == "RED": return True

def EXIT_SHORT_CONDITION(klines, low, mid, high):
    if (binance_futures_api.candle_body(klines) > binance_futures_api.previous_candle_body(klines) or \
        binance_futures_api.current_close(klines) > EMA.LOWEST(low, mid, high) or EMA.UPWARD_MOVEMENT(low)) and \
        binance_futures_api.candle_color(klines) == "GREEN": return True

# ==========================================================================================================================================================================
#                                                    DEPLOY THE BOT
# ==========================================================================================================================================================================

import requests, socket, urllib3
from binance.exceptions import BinanceAPIException
from apscheduler.schedulers.blocking import BlockingScheduler

if config.live_trade:
    print(colored("LIVE TRADE IS ENABLED\n", "green"))
else: print(colored("THIS IS BACKTESTING\n", "red"))

def add_this_to_cron_job():
    for i in range(len(config.coin)): lets_make_some_money(i)

try:
    if config.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(add_this_to_cron_job, 'cron', minute='0,30')
        scheduler.start()
    else: add_this_to_cron_job()

except (socket.timeout,
        BinanceAPIException,
        urllib3.exceptions.ProtocolError,
        urllib3.exceptions.ReadTimeoutError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        ConnectionResetError, KeyError, OSError) as e: print(e)

except KeyboardInterrupt: print("\n\nAborted.\n")

# def EXIT_LONG_CONDITION(klines, low, mid, high):
#     if (binance_futures_api.strong_candle(klines) or binance_futures_api.current_close(klines) < EMA.HIGHEST(low, mid, high) or \
#         binance_futures_api.upper_wick(klines) > binance_futures_api.candle_body(klines) + binance_futures_api.lower_wick(klines)) and \
#         binance_futures_api.candle_color(klines) == "RED": return True

# def EXIT_SHORT_CONDITION(klines, low, mid, high):
#     if  EMA.DELTA_UPWARD(low, mid, high) and \
#         binance_futures_api.strong_candle(klines) or \
#         binance_futures_api.lower_wick(klines) > binance_futures_api.candle_body(klines) + binance_futures_api.upper_wick(klines)) or \
#         binance_futures_api.current_close(klines) > EMA.LOWEST(low, mid, high) and \
#         binance_futures_api.candle_color(klines) == "GREEN": return True
