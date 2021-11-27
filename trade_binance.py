import config
import strategy
import api_binance
from datetime import datetime
from termcolor import colored

def lets_make_some_money():
    for i in range(len(config.pair)):
        pair = config.pair[i]
        leverage = config.leverage[i]
        quantity = config.quantity[i]

        print(pair)
        response = api_binance.position_information(pair)
        long_term_low_leverage = strategy.long_term_low_leverage(pair)
        # print(long_term_low_leverage)

        if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
        if int(response[0].get("leverage")) != leverage: api_binance.change_leverage(pair, leverage)
        
        if api_binance.LONG_SIDE(response) == "NO_POSITION":
            if long_term_low_leverage["BUY"].iloc[-1]:
                api_binance.trailing_open_long(pair, quantity)
            else: print("_LONG_SIDE : 🐺 WAIT 🐺")

        if api_binance.LONG_SIDE(response) == "LONGING":
            if long_term_low_leverage["SELL"].iloc[-1]:
                api_binance.market_close_long(pair, response)
                api_binance.cancel_all_open_orders(pair)
            else: print(colored("_LONG_SIDE : HOLDING_LONG", "green"))

        if api_binance.SHORT_SIDE(response) == "NO_POSITION":
            if long_term_low_leverage["SELL"].iloc[-1]:
                api_binance.trailing_open_short(pair, quantity)
            else: print("SHORT_SIDE : 🐺 WAIT 🐺")

        if api_binance.SHORT_SIDE(response) == "SHORTING":
            if long_term_low_leverage["BUY"].iloc[-1]:
                api_binance.market_close_short(pair, response)
                api_binance.cancel_all_open_orders(pair)
            else: print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))
            
        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS A SHOWCASE\n", "red")) 

try: lets_make_some_money()
except KeyboardInterrupt: print("\n\nAborted.\n")
