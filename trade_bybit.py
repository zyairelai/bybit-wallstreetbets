import bybit_api
import config, EMA
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    print(bybit_api.pair[i])
    klines   = bybit_api.KLINE_INTERVAL_1DAY(i)
    response = bybit_api.position_information(i)
    dataset  = bybit_api.closing_price_list(klines)

    low  = EMA.compute(5, dataset)
    mid  = EMA.compute(8, dataset)
    high = EMA.compute(13, dataset)

    leverage = bybit_api.leverage[i]
    if response[0].get('leverage') != leverage: bybit_api.change_leverage(i, leverage)
    if response[1].get('leverage') != leverage: bybit_api.change_leverage(i, leverage)
    if not response[0].get('is_isolated'): bybit_api.change_margin_to_ISOLATED(i, leverage)
    if not response[1].get('is_isolated'): bybit_api.change_margin_to_ISOLATED(i, leverage)

    if bybit_api.LONG_SIDE(response) == "NO_POSITION":
        if GO_LONG_CONDITION(klines, low, mid, high):
            bybit_api.open_long_position(i)
            print(colored("🚀 GO_LONG 🚀", "green"))
        else: print("LONG_SIDE : 🐺 WAIT 🐺")

    if bybit_api.LONG_SIDE(response) == "LONGING":
        if EXIT_LONG_CONDITION(klines, low, mid, high):
            bybit_api.close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("HOLDING_LONG", "green"))

    if bybit_api.SHORT_SIDE(response) == "NO_POSITION":
        if GO_SHORT_CONDITION(klines, low, mid, high):
            bybit_api.open_short_position(i)
            print(colored("💥 GO_SHORT 💥", "red"))
        else: print("SHORT_SIDE : 🐺 WAIT 🐺")

    if bybit_api.SHORT_SIDE(response) == "SHORTING":
        if EXIT_SHORT_CONDITION(klines, low, mid, high):
            bybit_api.close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("HOLDING_SHORT", "red"))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                    ENTRY CONDITIONS
# ==========================================================================================================================================================================

def GO_LONG_CONDITION(klines, low, mid, high):
    if not EMA.ABSOLUTE_DOWNTREND(low, mid, high) and EMA.DELTA_UPWARD(low, mid, high) and \
        bybit_api.strong_candle(klines) and \
        bybit_api.candle_color(klines) == "GREEN" and \
        bybit_api.current_close(klines) > EMA.MIDDLE(low, mid, high): return True

def GO_SHORT_CONDITION(klines, low, mid, high):
    if not EMA.ABSOLUTE_UPTREND(low, mid, high) and EMA.DELTA_DOWNWARD(low, mid, high) and \
        bybit_api.strong_candle(klines) and \
        bybit_api.candle_color(klines) == "RED" and \
        bybit_api.current_close(klines) < EMA.MIDDLE(low, mid, high): return True

def EXIT_LONG_CONDITION(klines, low, mid, high):
    if (bybit_api.upper_wick > bybit_api.candle_body + bybit_api.lower_wick) or \
        bybit_api.current_close(klines) < EMA.HIGHEST(low, mid, high) and \
        bybit_api.candle_color(klines) == "RED": return True

def EXIT_SHORT_CONDITION(klines, low, mid, high):
    if (bybit_api.lower_wick > bybit_api.candle_body + bybit_api.upper_wick) or \
        bybit_api.current_close(klines) > EMA.LOWEST(low, mid, high) and \
        bybit_api.candle_color(klines) == "GREEN": return True

# ==========================================================================================================================================================================
#                                                    DEPLOY THE BOT
# ==========================================================================================================================================================================

import requests, socket, urllib3
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
