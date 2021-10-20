import config
import strategy
import api_bybit
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    dataset = strategy.dataset(i)
    response = api_bybit.position_information(i)
    if response[0].get('leverage') != config.leverage[i]: api_bybit.change_leverage(i)
    if response[1].get('leverage') != config.leverage[i]: api_bybit.change_leverage(i)
    if not response[0].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i)
    if not response[1].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i)

    api_bybit.cancle_all_active_order(i)

    if api_bybit.LONG_SIDE(response) == "NO_POSITION":
        if strategy.GO_LONG_CONDITION(dataset):
            api_bybit.market_open_long(i) if config.market_order else api_bybit.limit_open_long(i)
            print(colored("🚀 GO_LONG 🚀", "green"))
        else: print("LONG_SIDE : 🐺 WAIT 🐺")

    if api_bybit.LONG_SIDE(response) == "LONGING":
        if strategy.EXIT_LONG_CONDITION(dataset):
            api_bybit.market_close_long(i, response) if config.market_order else api_bybit.limit_close_long(i, response)
            print("💰 CLOSE_LONG 💰")
        else: print(colored("HOLDING_LONG", "green"))

    if api_bybit.SHORT_SIDE(response) == "NO_POSITION":
        if strategy.GO_SHORT_CONDITION(dataset):
            api_bybit.market__open_short(i) if config.market_order else api_bybit.limit_open_short(i)
            print(colored("💥 GO_SHORT 💥", "red"))
        else: print("SHORT_SIDE : 🐺 WAIT 🐺")

    if api_bybit.SHORT_SIDE(response) == "SHORTING":
        if strategy.EXIT_SHORT_CONDITION(dataset):
            api_bybit.market_close_short(i, response) if config.market_order else api_bybit.limit_close_short(i, response)
            print("💰 CLOSE_SHORT 💰")
        else: print(colored("HOLDING_SHORT", "red"))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                    DEPLOY THE BOT
# ==========================================================================================================================================================================

import requests, socket, urllib3
from apscheduler.schedulers.blocking import BlockingScheduler

if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
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
