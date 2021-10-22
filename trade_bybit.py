import api_bybit
import config, strategy
from datetime import datetime
from termcolor import colored
from apscheduler.schedulers.blocking import BlockingScheduler

if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
else: print(colored("THIS IS BACKTESTING\n", "red"))

def lets_make_some_money():
    for i in range(len(config.coin)):
        klines_4HOUR = strategy.klines_4HOUR(i)
        bitcoin = strategy.Moving_Average_of_Bitcoin()
        response = api_bybit.position_information(i)
        if response[0].get('leverage') != config.leverage[i]: api_bybit.change_leverage(i)
        if response[1].get('leverage') != config.leverage[i]: api_bybit.change_leverage(i)
        if not response[0].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i)
        if not response[1].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i)

        if api_bybit.LONG_SIDE(response) == "NO_POSITION":
            if strategy.GO_LONG_CONDITION(klines_4HOUR, bitcoin):
                api_bybit.market_open_long(i)
                print(colored("🚀 GO_LONG 🚀", "green"))
            else: print("LONG_SIDE  : 🐺 WAIT 🐺")

        if api_bybit.LONG_SIDE(response) == "LONGING":
            if strategy.EXIT_LONG_CONDITION(klines_4HOUR, bitcoin):
                api_bybit.market_close_long(i, response)
                print("💰 CLOSE_LONG 💰")
            else: print(colored("HOLDING_LONG", "green"))

        if api_bybit.SHORT_SIDE(response) == "NO_POSITION":
            if strategy.GO_SHORT_CONDITION(klines_4HOUR, bitcoin):
                api_bybit.market_open_short(i)
                print(colored("💥 GO_SHORT 💥", "red"))
            else: print("SHORT_SIDE : 🐺 WAIT 🐺")

        if api_bybit.SHORT_SIDE(response) == "SHORTING":
            if strategy.EXIT_SHORT_CONDITION(klines_4HOUR, bitcoin):
                api_bybit.market_close_short(i, response)
                print("💰 CLOSE_SHORT 💰")
            else: print(colored("HOLDING_SHORT", "red"))

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    if config.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(lets_make_some_money, 'cron', minute='0,10,20,30,40,50')
        scheduler.start()
    else: lets_make_some_money()

except KeyboardInterrupt: print("\n\nAborted.\n")
