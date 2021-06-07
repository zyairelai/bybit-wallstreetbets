import config, EMA
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    print(binance_futures_api.pair[i])
    klines   = binance_futures_api.KLINE_INTERVAL_15MINUTE(i)
    response = binance_futures_api.position_information(i)
    dataset  = binance_futures_api.closing_price_list(klines)
    EMA_low  = EMA.compute(3, dataset)
    EMA_high = EMA.compute(7, dataset)

    leverage = config.leverage
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if binance_futures_api.get_position_amount(i) > 0: # LONGING
        if EMA.BOTH_GOING_DOWN(EMA_low, EMA_high):
            binance_futures_api.close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("HOLDING_LONG", "green"))

    elif binance_futures_api.get_position_amount(i) < 0: # SHORTING
        if EMA.BOTH_GOING_UP(EMA_low, EMA_high):
            binance_futures_api.close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("HOLDING_SHORT", "red"))

    else:
        if EMA.ALL_GOING_UP(EMA_low, EMA_high):
            binance_futures_api.open_long_position(i)
            print(colored("🚀 GO_LONG 🚀", "green"))

        elif EMA.ALL_GOING_DOWN(EMA_low, EMA_high):
            binance_futures_api.open_short_position(i)
            print(colored("💥 GO_SHORT 💥", "red"))

        else: print("🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

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
        scheduler.add_job(add_this_to_cron_job, 'cron', second='0')
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
