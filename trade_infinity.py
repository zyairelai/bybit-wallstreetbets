import config
import strategy
import api_binance
from pytz import utc
from datetime import datetime
from termcolor import colored
from apscheduler.schedulers.blocking import BlockingScheduler

def lets_make_some_money():
    for i in range(len(config.pair)):
        pair = config.pair[i]
        leverage = config.leverage[i]
        quantity = config.quantity[i]
        trailing = config.use_trailing

        print(pair)
        response = api_binance.position_information(pair)
        long_term_low_leverage = strategy.long_term_low_leverage(pair)
        # print(long_term_low_leverage)

        if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
        if int(response[0].get("leverage")) != leverage: api_binance.change_leverage(pair, leverage)

        if long_term_low_leverage["BUY"].iloc[-1]:
            api_binance.market_close_short(pair, response
            api_binance.market_open_long(pair, quantity))
            api_binance.cancel_all_open_orders(pair)

        if long_term_low_leverage["SELL"].iloc[-1]:
            api_binance.market_close_long(pair, response)
            api_binance.market_open_short(pair, quantity)
            api_binance.cancel_all_open_orders(pair)

        if api_binance.LONG_SIDE(response)  == "NO_POSITION" : print("_LONG_SIDE : 🐺 NO POSITION 🐺")
        if api_binance.LONG_SIDE(response)  == "LONGING"     : print(colored("_LONG_SIDE : HOLDING_LONG", "green"))
        if api_binance.SHORT_SIDE(response) == "NO_POSITION" : print("SHORT_SIDE : 🐺 NO POSITION 🐺")
        if api_binance.SHORT_SIDE(response) == "SHORTING"    : print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS A SHOWCASE\n", "red")) 

if config.live_trade and config.enable_scheduler:
    scheduler = BlockingScheduler()
    scheduler.add_job(lets_make_some_money, 'cron', hour='0', timezone=utc)
    scheduler.start()
else:
    lets_make_some_money()
