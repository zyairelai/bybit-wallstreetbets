import config, ccxt, pandas
ccxt_client = ccxt.bybit()

query = 100
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
big_timeframe   = '4h'
entry_timeframe = '1h'

def retrieve_klines(i):
    return pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], entry_timeframe, limit=query), columns=tohlcv_column)

def Moving_Average(i):
    klines = pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], big_timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = klines["timestamp"]
    moving_average['MA'] = klines["close"].rolling(window=50).mean()
    return moving_average

def swing_trade(i, klines):
    self_MA = Moving_Average(i)
    klines = pandas.merge_asof(klines, self_MA, on='timestamp')
    klines['high_s2'] = klines["high"].shift(2)
    klines['high_s3'] = klines["high"].shift(3)
    klines['low_s2'] = klines["low"].shift(2)
    klines['low_s3'] = klines["low"].shift(3)

    # Backtest trades
    klines["GO_LONG"] = klines.apply(GO_LONG_CONDITION, axis=1)
    klines["GO_SHORT"] = klines.apply(GO_SHORT_CONDITION, axis=1)
    klines["EXIT_LONG"] = klines.apply(EXIT_LONG_CONDITION, axis=1)
    klines["EXIT_SHORT"] = klines.apply(EXIT_SHORT_CONDITION, axis=1)

    return klines

def GO_LONG_CONDITION(klines):
    return True if (klines['open'] > klines['high_s2'] and klines['open'] > klines['high_s3']) and klines['open'] > klines['MA'] else False

def GO_SHORT_CONDITION(klines):
    return True if (klines['open'] < klines['low_s2'] and klines['open'] < klines['low_s3']) and klines['open'] < klines['MA'] else False

def EXIT_LONG_CONDITION(klines):
    return True if (klines['open'] < klines['low_s2'] and klines['open'] < klines['low_s3']) or klines['open'] < klines['MA'] else False

def EXIT_SHORT_CONDITION(klines):
    return True if (klines['open'] > klines['high_s2'] and klines['open'] > klines['high_s3']) or klines['open'] > klines['MA'] else False
