import config
import ccxt
import pandas

query = 200
exchange = ccxt.binance()
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

big_timeframe   = '12h'
entry_timeframe = '2h'

def retrieve_klines(i):
    return pandas.DataFrame(exchange.fetch_ohlcv(config.pair[i], entry_timeframe, limit=query), columns=tohlcv_column)

def Moving_Average(i):
    MA_threshold = 50
    klines = pandas.DataFrame(exchange.fetch_ohlcv(config.pair[i], big_timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = klines["timestamp"]
    moving_average['MA'] = klines["close"].rolling(window=MA_threshold).mean()
    moving_average["color"] = klines.apply(candle_color, axis=1)
    return moving_average

def candle_color(candle):
    if candle['close'] > candle['open']: return "GREEN"
    elif candle['close'] < candle['open']: return "RED"
    else: return "INDECISIVE"

print("_Big_ Timeframe : " + big_timeframe)
print("Entry Timeframe : " + entry_timeframe + "\n")