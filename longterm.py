live_trade = True

import os, numpy, time
from binance.client import Client
from datetime import datetime
from termcolor import colored
from apscheduler.schedulers.blocking import BlockingScheduler
def timestamp(): return int(time.time() * 1000)

pairname = "BTC" + "USDT"
amount = 0.001
leverage = 50

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)
client.futures_change_leverage(symbol=pairname, leverage=leverage, timestamp=timestamp())

def previous_EMA(length): return calculate_EMA(length)[-2]
def current_EMA(length) : return calculate_EMA(length)[-1]

def calculate_EMA(length):
    klines = client.futures_klines(symbol=pairname, limit=10, interval=Client.KLINE_INTERVAL_1HOUR)
    closing_price_list = []
    for candle in range(len(klines)):
        closing_price_list.append(float(klines[candle][4]))

    dataset = closing_price_list
    weights = numpy.exp(numpy.linspace(-1.,0.,length))
    weights /= weights.sum()
    a = numpy.convolve(dataset,weights)[:len(dataset)]
    a[:length]=a[length]
    return a

