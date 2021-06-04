import EMA
import api_bybit
import config_bybit
from datetime import datetime
from termcolor import colored
from apscheduler.schedulers.blocking import BlockingScheduler

EMA_length = 5
live_trade = config_bybit.live_trade

def lets_make_some_money(i):
    klines = api_bybit.KLINE_INTERVAL_1HOUR(i)
    dataset = api_bybit.closing_price_list(klines)
    response = api_bybit.position_information(i)
    EMA_list = EMA.compute(EMA_length, dataset)

    if live_trade: # Initial Setup
        leverage = config_bybit.leverage
        if response[0].get('leverage') != leverage: api_bybit.change_leverage(i, leverage)
        if response[1].get('leverage') != leverage: api_bybit.change_leverage(i, leverage)
        if not response[0].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i, leverage)
        if not response[1].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i, leverage)

    print(api_bybit.pair[i])

    if EMA.current(EMA_list) > EMA.previous(EMA_list):
        if live_trade:
            if api_bybit.LONG_SIDE(response) == "NO_POSITION": api_bybit.open_long_position(i)
            if api_bybit.SHORT_SIDE(response) == "SHORTING": api_bybit.close_short(i)
        print(colored("🚀 TO_THE_MOON 🚀", "green"))

    elif EMA.current(EMA_list) < EMA.previous(EMA_list):
        if live_trade:
            if api_bybit.SHORT_SIDE(response) == "NO_POSITION": api_bybit.open_short_position(i)
            if api_bybit.LONG_SIDE(response)  == "LONGING": api_bybit.close_long(i)
        print(colored("💥 TO_THE_MARS 💥", "red"))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def run_the_job():
    lets_make_some_money(0)

scheduler = BlockingScheduler()
scheduler.add_job(run_the_job, 'cron', second='0')
scheduler.start()
