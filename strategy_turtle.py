def swing_trade(i, klines):
    klines['55_MA'] = klines["close"].rolling(window=55).mean()
    klines['20_MA'] = klines["close"].rolling(window=20).mean()

    # Backtest trades
    klines["GO_LONG"] = klines.apply(GO_LONG_CONDITION, axis=1)
    klines["GO_SHORT"] = klines.apply(GO_SHORT_CONDITION, axis=1)
    klines["EXIT_LONG"] = klines.apply(EXIT_LONG_CONDITION, axis=1)
    klines["EXIT_SHORT"] = klines.apply(EXIT_SHORT_CONDITION, axis=1)

    return klines

def GO_LONG_CONDITION(klines):
    return True if klines['open'] > klines['55_MA'] and klines['open'] > klines['20_MA'] else False

def GO_SHORT_CONDITION(klines):
    return True if klines['open'] < klines['55_MA'] and klines['open'] < klines['20_MA'] else False

def EXIT_LONG_CONDITION(klines):
    return True if klines['open'] < klines['20_MA'] else False

def EXIT_SHORT_CONDITION(klines):
    return True if klines['open'] > klines['20_MA'] else False
