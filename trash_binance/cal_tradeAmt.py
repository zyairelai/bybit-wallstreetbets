import time
from binance.client import Client

client = Client("api_key", "api_secret")

coin = input("\nEnter Coin Symbol (eg. BTC, ETH, BNB...) : ").upper() or "BTC"
trade_size_in_usdt = input("\nEnter Your Trade Amount in USDT : ") or 100

def get_timestamp():
    return int(time.time() * 1000)

def mark_price():
    return float(client.futures_mark_price(symbol=coin+"USDT", timestamp=get_timestamp()).get('markPrice'))

def leverage(markPrice):
    if   markPrice < 1: leverage = 5
    elif markPrice < 10: leverage = 10
    elif markPrice < 100: leverage = 15
    elif markPrice < 1000: leverage = 20
    elif markPrice < 10000: leverage = 25
    else: leverage = 30
    return int(leverage)

current_market_price = mark_price()
default_leverage = leverage(current_market_price)
trade_amount_in_coin = round((float(trade_size_in_usdt) * default_leverage / current_market_price), 6)
print("\nDefault Leverage : " + str(default_leverage) + "x")
print("\nTrade Quantity : " + str(trade_amount_in_coin) + " " + coin)
print()
