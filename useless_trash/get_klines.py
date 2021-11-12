import ccxt
import pandas

query = 1000
exchange = ccxt.binance()
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

big_timeframe   = '12h'
entry_timeframe = '1h'

def get_klines(pair):
    return pandas.DataFrame(exchange.fetch_ohlcv(pair, entry_timeframe, limit=query), columns=tohlcv_column)

def Bitcoin_trend():
    threshold = 50
    bitcoin_klines = pandas.DataFrame(exchange.fetch_ohlcv("BTCUSDT", big_timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = bitcoin_klines["timestamp"]
    moving_average['BTC_50EMA'] = bitcoin_klines['close'].ewm(span=threshold).mean()
    moving_average['BTC_CLOSE'] = bitcoin_klines["close"]

    def btc_trend(moving_average):
        if   moving_average['BTC_CLOSE'] > moving_average['BTC_50EMA']: return "uptrend"
        elif moving_average['BTC_CLOSE'] < moving_average['BTC_50EMA']: return "downtrend"

    moving_average['Bitcoin'] = moving_average.apply(btc_trend, axis=1)
    moving_average = moving_average.drop(['BTC_50EMA', 'BTC_CLOSE'], axis=1)
    return moving_average

def Moving_Average(pair):
    threshold = 50
    klines = pandas.DataFrame(exchange.fetch_ohlcv(pair, big_timeframe, limit=query), columns=tohlcv_column)
    moving_average = pandas.DataFrame()
    moving_average['timestamp'] = klines["timestamp"]
    moving_average['MA'] = klines['close'].ewm(span=threshold).mean()
    return moving_average

def trend(pair):
    klines = pandas.DataFrame(exchange.fetch_ohlcv(pair, big_timeframe, limit=query), columns=tohlcv_column)
    klines['8_EMA'] = klines['close'].ewm(span=8).mean()
    klines['13_EMA'] = klines['close'].ewm(span=13).mean()
    klines['21_EMA'] = klines['close'].ewm(span=21).mean()
    klines['12_EMA'] = klines['close'].ewm(span=12).mean()
    klines['26_EMA'] = klines['close'].ewm(span=26).mean()
    klines['MACD']   = klines['12_EMA'] - klines['26_EMA']
    klines['Signal'] = klines['MACD'].ewm(span=9).mean()
    klines['Histogram'] = klines['MACD'] - klines['Signal']

    def check_trend(klines):
        if  klines['8_EMA']  > klines['13_EMA'] and \
            klines['13_EMA'] > klines['21_EMA'] and \
            klines['Histogram'] > 0 : return "uptrend"

        elif klines['8_EMA']  < klines['13_EMA'] and \
             klines['13_EMA'] < klines['21_EMA'] and \
             klines['Histogram'] < 0 : return "downtrend"

        else: return "indecisive"

    klines['trend'] = klines.apply(check_trend, axis=1)
    klines = klines.drop(['8_EMA', '13_EMA', '21_EMA', '12_EMA', '26_EMA', 'MACD', 'Signal', 'Histogram'], axis=1)
    return klines

def entry(pair):
    klines = pandas.DataFrame(exchange.fetch_ohlcv(pair, entry_timeframe, limit=query), columns=tohlcv_column)
    klines['8_EMA'] = klines['close'].ewm(span=8).mean()
    klines['13_EMA'] = klines['close'].ewm(span=13).mean()
    klines['21_EMA'] = klines['close'].ewm(span=21).mean()
    klines['12_EMA'] = klines['close'].ewm(span=12).mean()
    klines['26_EMA'] = klines['close'].ewm(span=26).mean()
    klines['MACD']   = klines['12_EMA'] - klines['26_EMA']
    klines['Signal'] = klines['MACD'].ewm(span=9).mean()
    klines['Histogram'] = klines['MACD'] - klines['Signal']

    def check_trend(klines):
        if  klines['8_EMA']  > klines['13_EMA'] and \
            klines['13_EMA'] > klines['21_EMA'] and \
            klines['Histogram'] > 0 : return "uptrend"

        elif klines['8_EMA']  < klines['13_EMA'] and \
             klines['13_EMA'] < klines['21_EMA'] and \
             klines['Histogram'] < 0 : return "downtrend"

        else: return "indecisive"

    klines['entry'] = klines.apply(check_trend, axis=1)
    # klines = klines.drop(['8_EMA', '13_EMA', '21_EMA', '12_EMA', '26_EMA', 'MACD', 'Signal', 'Histogram'], axis=1)
    return klines

print("_Big_ Timeframe : " + big_timeframe)
print("Entry Timeframe : " + entry_timeframe)
# print(trend(0))