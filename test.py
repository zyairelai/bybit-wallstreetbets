import config
import binance_futures_api
from termcolor import colored
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

haha = False
live_trade = False

def calculating_EMA(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def get_closing_price_list(klines):
    closing_price_list = []
    for candle in range(len(klines)):
        closing_price_list.append(float(klines[candle][4]))
    return closing_price_list


response = binance_futures_api.position_information()
position_Amt = binance_futures_api.get_position_amount()
klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR()

dataset = get_closing_price_list(klines_1HOUR)
ema3 = calculating_EMA(3, dataset)
ema7 = calculating_EMA(7, dataset)

# for each in ema3: print(colored(each, "green"))
for each in ema7: print(colored(each, "yellow"))
print()