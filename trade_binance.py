import config
import strategy
import api_binance
from datetime import datetime
from termcolor import colored

callbackRate = 2

def lets_make_some_money(pair, leverage, quantity): 
    print(pair)
    response = api_binance.position_information(pair)
    if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
    if int(response[0].get("leverage")) != leverage: api_binance.change_leverage(pair, leverage)
    long_term_low_leverage = strategy.swing_trade(pair)
    # print(long_term_low_leverage)

    if api_binance.LONG_SIDE(response) == "NO_POSITION":
        if long_term_low_leverage["GO_LONG"].iloc[-1]:
            api_binance.trailing_open_long(pair, quantity, callbackRate)
        else: print("_LONG_SIDE : 🐺 WAIT 🐺")

    if api_binance.LONG_SIDE(response) == "LONGING":
        if 'EXIT_LONG' in long_term_low_leverage.columns:
            if long_term_low_leverage["EXIT_LONG"].iloc[-1]:
                api_binance.market_close_long(pair, response)
                api_binance.cancel_all_open_orders(pair)
            else: print(colored("_LONG_SIDE : HOLDING_LONG", "green"))

    if api_binance.SHORT_SIDE(response) == "NO_POSITION":
        if long_term_low_leverage["GO_SHORT"].iloc[-1]:
            api_binance.trailing_open_short(pair, quantity, callbackRate)
        else: print("SHORT_SIDE : 🐺 WAIT 🐺")

    if api_binance.SHORT_SIDE(response) == "SHORTING":
        if 'EXIT_SHORT' in long_term_low_leverage.columns:
            if long_term_low_leverage["EXIT_SHORT"].iloc[-1]:
                api_binance.market_close_short(pair, response)
                api_binance.cancel_all_open_orders(pair)
            else: print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))
        
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS BACKTESTING\n", "red")) 

try:
    for i in range(len(config.pair)):
        pair     = config.pair[i]
        leverage = config.leverage[i]
        quantity = config.quantity[i]
        lets_make_some_money(pair, leverage, quantity)
except KeyboardInterrupt: print("\n\nAborted.\n")
