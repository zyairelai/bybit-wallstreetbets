import config
import longterm
import requests
import socket
import urllib3
from termcolor import colored
from binance.exceptions import BinanceAPIException
from apscheduler.schedulers.blocking import BlockingScheduler

if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
else: print(colored("THIS IS BACKTESTING\n", "red"))

def long_term_low_leverage():
    for i in range(len(config.coin)):
        longterm.lets_make_some_money(i)

try:
    if config.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(long_term_low_leverage, 'cron', second='0')
        scheduler.start()
    else: long_term_low_leverage()

except (socket.timeout,
        BinanceAPIException,
        urllib3.exceptions.ProtocolError,
        urllib3.exceptions.ReadTimeoutError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        ConnectionResetError, KeyError, OSError) as e: print(e)

except KeyboardInterrupt: print("\n\nAborted.\n")
