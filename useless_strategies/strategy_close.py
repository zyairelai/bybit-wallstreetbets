import pandas
import get_klines

def swing_trade(i, klines):
    bitcoin = get_klines.Bitcoin_trend()
    # self_MA = get_klines.Moving_Average(i)
    # klines = pandas.merge_asof(klines, self_MA, on='timestamp')
    klines = pandas.merge_asof(klines, bitcoin, on='timestamp')
    klines['high_s1'] = klines["high"].shift(1)
    klines['high_s2'] = klines["high"].shift(2)
    klines['low_s1'] = klines["low"].shift(1)
    klines['low_s2'] = klines["low"].shift(2)

    # Backtest trades
    klines["GO_LONG"] = klines.apply(GO_LONG_CONDITION, axis=1)
    klines["GO_SHORT"] = klines.apply(GO_SHORT_CONDITION, axis=1)
    klines["EXIT_LONG"] = klines.apply(EXIT_LONG_CONDITION, axis=1)
    klines["EXIT_SHORT"] = klines.apply(EXIT_SHORT_CONDITION, axis=1)

    klines = klines.drop(['high_s1', 'high_s2', 'low_s1', 'low_s2'], axis=1)
    return klines

def GO_LONG_CONDITION(klines):
    if klines['Bitcoin'] == "uptrend" and klines['close'] > klines['high_s1']: return True
    else: return False

def GO_SHORT_CONDITION(klines):
    if klines['Bitcoin'] == "downtrend" and klines['close'] < klines['low_s1'] : return True
    else: return False

def EXIT_LONG_CONDITION(klines):
    return True if klines['close'] < klines['low_s2'] else False

def EXIT_SHORT_CONDITION(klines):
    return True if klines['close'] > klines['high_s2'] else False
