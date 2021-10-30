import api_binance
import config
import strategy
import retrieve_klines
from termcolor import colored
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS A DEMO\n", "red"))

def lets_make_some_money():
    for i in range(len(config.coin)):    
        print(config.pair[i])
        klines = retrieve_klines.retrieve_klines(i)
        swing_trades = strategy.swing_trade(i, klines)
        swing_trades = swing_trades.drop(['volume'], axis=1)
        # print(swing_trades)

        response = api_binance.position_information(i)
        if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(i)
        if int(response[0].get("leverage")) != config.leverage[i]: api_binance.change_leverage(i)
        
        if api_binance.LONG_SIDE(response) == "NO_POSITION":
            if swing_trades["GO_LONG"].iloc[-1]: api_binance.market_open_long(i)
            else: print("_LONG_SIDE : 🐺 WAIT 🐺")

        if api_binance.LONG_SIDE(response) == "LONGING":
            if swing_trades["EXIT_LONG"].iloc[-1]: api_binance.market_close_long(i, response)
            else: print(colored("_LONG_SIDE : HOLDING_LONG", "green"))

        if api_binance.SHORT_SIDE(response) == "NO_POSITION":
            if swing_trades["GO_SHORT"].iloc[-1]: api_binance.market_open_short(i)
            else: print("SHORT_SIDE : 🐺 WAIT 🐺")

        if api_binance.SHORT_SIDE(response) == "SHORTING":
            if swing_trades["EXIT_SHORT"].iloc[-1]: api_binance.market_close_short(i, response)
            else: print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    if config.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(lets_make_some_money, 'cron', minute='1')
        scheduler.start()
    else: lets_make_some_money()

except KeyboardInterrupt: print("\n\nAborted.\n")
