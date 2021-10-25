import config
import ccxt
import pandas

query = 200
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

big_timeframe   = '4h'
entry_timeframe = '1h'

def retrieve_klines(i):
    return pandas.DataFrame(ccxt.binance().fetch_ohlcv(config.pair[i], entry_timeframe, limit=query), columns=tohlcv_column)

def Moving_Average(i):
    klines = pandas.DataFrame(ccxt.binance().fetch_ohlcv(config.pair[i], big_timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = klines["timestamp"]
    moving_average['MA'] = klines["close"].rolling(window=50).mean()
    return moving_average
