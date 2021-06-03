import bybit_api, config, EMA
from termcolor import colored
from datetime import datetime

i = 0
live_trade = config.live_trade
lower_EMA  = config.lower_EMA
higher_EMA = config.higher_EMA

klines = bybit_api.get_klines(i)
dataset = bybit_api.closing_price_list(klines)

low_EMA_list  = EMA.compute(lower_EMA, dataset)
high_EMA_list = EMA.compute(higher_EMA, dataset)

current_ema_low   = EMA.current(low_EMA_list)
current_ema_high  = EMA.current(high_EMA_list)

print(bybit_api.position_information(i))
