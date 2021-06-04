import EMA
import config_binance
import api_binance_futures
from datetime import datetime
from termcolor import colored
from apscheduler.schedulers.blocking import BlockingScheduler

live_trade = config_binance.live_trade
EMA_length  = 5

def lets_make_some_money(i):
    klines = api_binance_futures.KLINE_INTERVAL_1DAY(i)
    dataset = api_binance_futures.get_closing_price_list(klines)
    response = api_binance_futures.position_information(i)[0]
    EMA_list = EMA.compute(EMA_length, dataset)

    if live_trade: # Initial Setup
        leverage = config_binance.leverage
        if int(response.get("leverage")) != leverage: api_binance_futures.change_leverage(i, leverage)
        if response.get('marginType') != "isolated": api_binance_futures.change_margin_to_ISOLATED(i)

    print(api_binance_futures.pair[i])
    if api_binance_futures.get_position_amount(i) > 0:
        if EMA.current(EMA_list) < EMA.previous(EMA_list):
            if live_trade: api_binance_futures.close_long(i)
            print("ACTION           :   💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif api_binance_futures.get_position_amount(i) < 0:
        if EMA.current(EMA_list) > EMA.previous(EMA_list):
            if live_trade: api_binance_futures.close_short(i)
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if EMA.current(EMA_list) > EMA.previous(EMA_list):
            if live_trade: api_binance_futures.open_long_position(i)
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif EMA.current(EMA_list) < EMA.previous(EMA_list):
            if live_trade: api_binance_futures.open_short_position(i)
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def run_the_job():
    lets_make_some_money(0)

scheduler = BlockingScheduler()
scheduler.add_job(run_the_job, 'cron', second='0')
scheduler.start()