import bybit_api
import candlestick
import config, EMA
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    print(bybit_api.pair[i])
    bybit_api.cancle_all_active_order(i)
    klines   = bybit_api.KLINE_INTERVAL_1DAY(i)
    response = bybit_api.position_information(i)
    dataset  = candlestick.closing_price_list(klines)
    decimal  = candlestick.price_decimal_place(klines)

    low  = EMA.compute(8, dataset, decimal)
    mid  = EMA.compute(13, dataset, decimal)
    high = EMA.compute(21, dataset, decimal)

    leverage = bybit_api.leverage[i]
    if response[0].get('leverage') != leverage: bybit_api.change_leverage(i, leverage)
    if response[1].get('leverage') != leverage: bybit_api.change_leverage(i, leverage)
    if not response[0].get('is_isolated'): bybit_api.change_margin_to_ISOLATED(i, leverage)
    if not response[1].get('is_isolated'): bybit_api.change_margin_to_ISOLATED(i, leverage)

    if bybit_api.LONG_SIDE(response) == "NO_POSITION":
        if not EMA.ABSOLUTE_DOWNTREND(low, mid, high) and EMA.DELTA_UPWARD(low, mid, high) and candlestick.candle_color(klines) == "GREEN":
            bybit_api.limit_open_long(i, GO_LONG_PRICE(klines))
            print(colored("🚀 GO_LONG 🚀", "green"))
        else: print("LONG_SIDE : 🐺 WAIT 🐺")

    if bybit_api.LONG_SIDE(response) == "LONGING":
        if candlestick.candle_color(klines) == "RED":
            bybit_api.limit_close_long(i, response, EXIT_LONG_PRICE(klines, low, mid, high))
        else: print(colored("HOLDING_LONG", "green"))

    if bybit_api.SHORT_SIDE(response) == "NO_POSITION":
        if not EMA.ABSOLUTE_UPTREND(low, mid, high) and EMA.DELTA_DOWNWARD(low, mid, high) and candlestick.candle_color(klines) == "RED":
            bybit_api.limit_open_short(i, GO_SHORT_PRICE(klines))
            print(colored("💥 GO_SHORT 💥", "red"))
        else: print("SHORT_SIDE : 🐺 WAIT 🐺")

    if bybit_api.SHORT_SIDE(response) == "SHORTING":
        if candlestick.candle_color(klines) == "GREEN":
            bybit_api.limit_close_short(i, response, EXIT_SHORT_PRICE(klines, low, mid, high))
        else: print(colored("HOLDING_SHORT", "red"))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                    ENTRY CONDITIONS
# ==========================================================================================================================================================================

def GO_LONG_PRICE(klines):
    if candlestick.previous_candle_color(klines) == "GREEN":
        if candlestick.current_close(klines) > candlestick.previous_high(klines): return candlestick.current_close(klines)
        else : return candlestick.previous_high(klines)
    elif candlestick.previous_candle_color(klines) == "RED":
        if   candlestick.current_close(klines) > candlestick.previous_high(klines): return candlestick.current_close(klines)
        elif candlestick.current_close(klines) > candlestick.previous_open(klines): return candlestick.previous_high(klines)
        else : return candlestick.previous_open(klines)

def GO_SHORT_PRICE(klines):
    if candlestick.previous_candle_color(klines) == "GREEN":
        if   candlestick.current_close(klines) < candlestick.previous_low(klines): return candlestick.current_close(klines)
        elif candlestick.current_close(klines) < candlestick.previous_open(klines): return candlestick.previous_low(klines)
        else : return candlestick.previous_open(klines)
    elif candlestick.previous_candle_color(klines) == "RED":
        if candlestick.current_close(klines) < candlestick.previous_low(klines): return candlestick.current_close(klines)
        else : return candlestick.previous_low(klines)

def EXIT_LONG_PRICE(klines, low, mid, high):
    if candlestick.previous_low(klines) > EMA.HIGHEST(low, mid, high):
        if candlestick.previous_candle_color == "GREEN": return candlestick.previous_low(klines)
        elif candlestick.previous_candle_color == "RED": return candlestick.previous_close(klines)
    else: return EMA.HIGHEST(low, mid, high)

def EXIT_SHORT_PRICE(klines, low, mid, high):
    if candlestick.previous_high(klines) < EMA.LOWEST(low, mid, high):
        if candlestick.previous_candle_color == "GREEN": return candlestick.previous_close(klines)
        elif candlestick.previous_candle_color == "RED": return candlestick.previous_high(klines)
    else: return EMA.LOWEST(low, mid, high)

# ==========================================================================================================================================================================
#                                                    DEPLOY THE BOT
# ==========================================================================================================================================================================

import requests
import socket
import urllib3
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
        urllib3.exceptions.ProtocolError,
        urllib3.exceptions.ReadTimeoutError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        ConnectionResetError, KeyError, OSError) as e: print(e)

except KeyboardInterrupt: print("\n\nAborted.\n")
