import pandas
import get_klines

def swing_trade(pair, klines):
    trend = get_klines.trend(pair)
    klines = pandas.merge_asof(klines, trend, on='timestamp')

    entry = get_klines.entry(pair)
    klines = pandas.merge_asof(klines, entry, on='timestamp')
    
    # Backtest trades
    klines["GO_LONG"] = klines.apply(GO_LONG_CONDITION, axis=1)
    klines["GO_SHORT"] = klines.apply(GO_SHORT_CONDITION, axis=1)
    klines["EXIT_LONG"] = klines.apply(EXIT_LONG_CONDITION, axis=1)
    klines["EXIT_SHORT"] = klines.apply(EXIT_SHORT_CONDITION, axis=1)

    return klines

def GO_LONG_CONDITION(klines):
    if  klines['trend'] == "uptrend" and \
        klines['8_EMA']  > klines['13_EMA'] and \
        klines['13_EMA'] > klines['21_EMA'] and \
        klines['Histogram'] > 0 : return True
    else: return False

def GO_SHORT_CONDITION(klines):
    if  klines['trend'] == "downtrend" and \
        klines['8_EMA']  < klines['13_EMA'] and \
        klines['13_EMA'] < klines['21_EMA'] and \
        klines['Histogram'] < 0 : return True
    else: return False

def EXIT_LONG_CONDITION(klines):
    if  klines['8_EMA']  < klines['13_EMA'] and \
        klines['13_EMA'] < klines['21_EMA'] and \
        klines['Histogram'] < 0 : return True
    else: return False

def EXIT_SHORT_CONDITION(klines):
    if  klines['8_EMA']  > klines['13_EMA'] and \
        klines['13_EMA'] > klines['21_EMA'] and \
        klines['Histogram'] > 0 : return True
    else: return False