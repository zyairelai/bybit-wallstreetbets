import config
import ccxt
import pandas

query = 200
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

big_timeframe   = '1d'
entry_timeframe = '6h'

def retrieve_klines(i):
    return pandas.DataFrame(ccxt.binance().fetch_ohlcv(config.pair[i], entry_timeframe, limit=query), columns=tohlcv_column)

def Moving_Average(i):
    klines = pandas.DataFrame(ccxt.binance().fetch_ohlcv(config.pair[i], big_timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = klines["timestamp"]
    moving_average['MA'] = klines["close"].rolling(window=50).mean()
    moving_average["color"] = klines.apply(candle_color, axis=1)
    return moving_average

def candle_color(candle):
    if candle['close'] > candle['open']: return "GREEN"
    elif candle['close'] < candle['open']: return "RED"
    else: return "INDECISIVE"
