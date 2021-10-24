import config, ccxt, pandas
ccxt_client = ccxt.bybit()

query = 100
follow_btc_trend = False
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

big___timeframe = '4h'
entry_timeframe = '1h'

def klines(i):
    print(config.pair[i])
    klines = pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], entry_timeframe, limit=query), columns=tohlcv_column)
    klines['color'] = klines.apply(candle_color, axis=1)
    return klines

def Moving_Average(i):
    bitcoin = pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], big___timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = bitcoin["timestamp"]
    moving_average['MA'] = bitcoin["close"].rolling(window=50).mean()
    return moving_average

def Moving_Average_of_Bitcoin():
    bitcoin = pandas.DataFrame(ccxt_client.fetch_ohlcv("BTC/USDT", big___timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = bitcoin["timestamp"]
    moving_average['btc_close'] = bitcoin["close"]
    moving_average['btc_MA'] = bitcoin["close"].rolling(window=50).mean()
    return moving_average

def swing_trade(i, klines):
    if follow_btc_trend:
        bitcoin = Moving_Average_of_Bitcoin()
        klines  = pandas.merge_asof(klines, bitcoin, on='timestamp')

    self_MA = Moving_Average(i)
    klines  = pandas.merge_asof(klines, self_MA, on='timestamp')    
    klines['high_s1'] = klines["high"].shift(1)
    klines['high_s2'] = klines["high"].shift(2)
    klines['low_s1'] = klines["low"].shift(1)
    klines['low_s2'] = klines["low"].shift(2)

    # Backtest trades
    klines["GO_LONG"] = klines.apply(GO_LONG_CONDITION, axis=1)
    klines["GO_SHORT"] = klines.apply(GO_SHORT_CONDITION, axis=1)
    klines["EXIT_LONG"] = klines.apply(EXIT_LONG_CONDITION, axis=1)
    klines["EXIT_SHORT"] = klines.apply(EXIT_SHORT_CONDITION, axis=1)
    return klines

def candle_color(klines):
    if klines['open'] > klines['close']: return "RED"
    elif klines['open'] < klines['close']: return "GREEN"
    else: return "INDECISIVE"

def GO_LONG_CONDITION(klines):
    if follow_btc_trend: return True if (klines['close'] > klines['high_s1'] and klines['close'] > klines['high_s2']) and klines['close'] > klines['MA'] and klines['btc_close'] > klines['btc_MA'] else False
    else: return True if (klines['close'] > klines['high_s1'] and klines['close'] > klines['high_s2']) and klines['close'] > klines['MA'] else False

def GO_SHORT_CONDITION(klines):
    if follow_btc_trend: return True if (klines['close'] < klines['low_s1'] and klines['close'] < klines['low_s2']) and klines['close'] < klines['MA'] and klines['btc_close'] < klines['btc_MA'] else False
    else: return True if (klines['close'] < klines['low_s1'] and klines['close'] < klines['low_s2']) and klines['close'] < klines['MA'] else False

def EXIT_LONG_CONDITION(klines):
    if follow_btc_trend: return True if (klines['close'] < klines['low_s1'] and klines['close'] < klines['low_s2']) or klines['close'] < klines['MA'] or klines['btc_close'] < klines['btc_MA'] else False
    else: return True if (klines['close'] < klines['low_s1'] and klines['close'] < klines['low_s2']) or klines['close'] < klines['MA'] else False

def EXIT_SHORT_CONDITION(klines):
    if follow_btc_trend: return True if (klines['close'] > klines['high_s1'] and klines['close'] > klines['high_s2']) or klines['close'] > klines['MA'] or klines['btc_close'] > klines['btc_MA'] else False
    else: return True if (klines['close'] > klines['high_s1'] and klines['close'] > klines['high_s2']) or klines['close'] > klines['MA'] else False
