import os, bybit, EMA, api_bybit, api_binance_futures
from termcolor import colored

api_key    = os.environ.get('BYBIT_API')
api_secret = os.environ.get('BYBIT_SECRET')
client     = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

i = 0
klines = api_binance_futures.KLINE_INTERVAL_1HOUR(i)
response = api_binance_futures.position_information(i)
dataset  = api_binance_futures.closing_price_list(klines)

EMA_low  = EMA.compute(3, dataset)
EMA_high = EMA.compute(7, dataset)

print(EMA.UP_TREND(EMA_low, EMA_high))
print(EMA.GOING_UP(EMA_low))
print(EMA.GOING_UP(EMA_high))

print(EMA.current(EMA_low))
print(EMA.current(EMA_high))

# for k in klines: print(k)