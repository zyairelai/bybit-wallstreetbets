import config
import api_bybit
from termcolor import colored
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS A DEMO\n", "red"))

import strategy
strategy = strategy

def lets_make_some_money():
    for i in range(len(config.pair)):
        pair = config.pair[i]
        leverage = config.leverage
        quantity = config.quantity[i]

        print(pair)
        klines = get_klines.get_klines(pair)
        swing_trades = strategy.swing_trade(pair, klines)
        swing_trades = swing_trades.drop(['volume'], axis=1)
        # print(swing_trades)

        response = api_bybit.position_information(pair)
        if response[0].get('leverage') != leverage: api_bybit.change_leverage(pair, leverage)
        if response[1].get('leverage') != leverage: api_bybit.change_leverage(pair, leverage)
        if not response[0].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(pair, leverage)
        if not response[1].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(pair, leverage)
        
        if api_bybit.LONG_SIDE(response) == "NO_POSITION":
            if swing_trades["GO_LONG"].iloc[-1]: api_bybit.market_open_long(pair, quantity)
            else: print("_LONG_SIDE : 🐺 WAIT 🐺")

        if api_bybit.LONG_SIDE(response) == "LONGING":
            if swing_trades["EXIT_LONG"].iloc[-1]: api_bybit.market_close_long(pair, response)
            else: print(colored("_LONG_SIDE : HOLDING_LONG", "green"))

        if api_bybit.SHORT_SIDE(response) == "NO_POSITION":
            if swing_trades["GO_SHORT"].iloc[-1]: api_bybit.market_open_short(pair, quantity)
            else: print("SHORT_SIDE : 🐺 WAIT 🐺")

        if api_bybit.SHORT_SIDE(response) == "SHORTING":
            if swing_trades["EXIT_SHORT"].iloc[-1]: api_bybit.market_close_short(pair, response)
            else: print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    if config.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(lets_make_some_money, 'cron', minute='1')
        scheduler.start()
    else: lets_make_some_money()

except KeyboardInterrupt: print("\n\nAborted.\n")
