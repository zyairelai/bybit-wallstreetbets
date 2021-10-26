import pandas
import retrieve_klines

def swing_trade(i, klines):
    self_MA = retrieve_klines.Moving_Average(i)
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

    klines = klines.drop(['high_s2', 'high_s3', 'low_s2', 'low_s3'], axis=1)
    return klines

def GO_LONG_CONDITION(klines):
    if  klines['open'] > klines['MA'] and \
        klines['open'] > klines['high_s2'] and \
        klines['open'] > klines['high_s3'] and \
        klines['color'] == "GREEN": return True
    else: return False

def GO_SHORT_CONDITION(klines):
    if  klines['open'] < klines['MA'] and \
        klines['open'] < klines['low_s2'] and \
        klines['open'] < klines['low_s3'] and \
        klines['color'] == "RED": return True
    else: return False

def EXIT_LONG_CONDITION(klines):
    return True if klines['open'] < klines['low_s2'] or klines['color'] == "RED" else False

def EXIT_SHORT_CONDITION(klines):
    return True if klines['open'] > klines['high_s2'] or klines['color'] == "GREEN" else False
