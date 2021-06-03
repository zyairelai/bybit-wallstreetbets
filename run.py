import sys, requests, socket, urllib3
from termcolor import colored
from binance.exceptions import BinanceAPIException
from apscheduler.schedulers.blocking import BlockingScheduler

bybit = sys.argv[-1] == "bybit"
binance = sys.argv[-1] == "binance"

def run_binance():
    import config_binance
    import longterm_binance

    if config_binance.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("THIS IS BACKTESTING\n", "red"))

    def making_money_from_binance():
        for i in range(len(config_binance.pair)):
            longterm_binance.lets_make_some_money(i)

    if config_binance.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(making_money_from_binance, 'cron', minute='0,20,40')
        scheduler.start()
    else: making_money_from_binance()

def run_bybit():
    import config_bybit
    import longterm_bybit

    if config_bybit.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("THIS IS BACKTESTING\n", "red"))

    def making_money_from_bybit():
        for i in range(len(config_bybit.pair)):
            longterm_bybit.lets_make_some_money(i)

    if config_bybit.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(making_money_from_bybit, 'cron', minute='0,20,40')
        scheduler.start()
    else: making_money_from_bybit()

def run():
    try:
        if binance:
            print(colored("\nTHE BOT IS RUNNING...\n", "green"))
            run_binance()
        elif bybit:
            print(colored("\nTHE BOT IS RUNNING...\n", "green"))
            run_bybit()
        else:
            print(colored("\nMAKE SURE YOU READ THE README.md 100 TIMES BEFORE YOU USE THE PROGRAM !!!\n", "red"))
            sys.exit()

    except (socket.timeout,
            BinanceAPIException,
            urllib3.exceptions.ProtocolError,
            urllib3.exceptions.ReadTimeoutError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout,
            ConnectionResetError, KeyError, OSError) as e: print(e)

    except KeyboardInterrupt: print("\n\nAborted.\n")

run()
