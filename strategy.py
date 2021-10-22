import config, ccxt, pandas
ccxt_client = ccxt.binance()

query = 100
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

def klines_4HOUR(i):
    print(config.pair[i])
    klines = pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '4h', limit=query), columns=tohlcv_column)
    klines['color'] = klines.apply(candle_color, axis=1)
    # print(klines)
    return klines

def Moving_Average_of_Bitcoin():
    bitcoin = pandas.DataFrame(ccxt_client.fetch_ohlcv("BTC/USDT", '1d', limit=query), columns=tohlcv_column)
    bitcoin['Moving_Avg'] = bitcoin["close"].rolling(window=50).mean()
    bitcoin = bitcoin.drop(['volume'], axis=1)
    # print(bitcoin)
    return bitcoin

def candle_color(klines):
    if klines['open'] > klines['close']: return "RED"
    elif klines['open'] < klines['close']: return "GREEN"
    else: return "INDECISIVE"

def GO_LONG_CONDITION(dataset, bitcoin):
    if (dataset['close'].iloc[-1] > dataset['close'].iloc[-2] and dataset['close'].iloc[-1] > dataset['close'].iloc[-3]) and \
        bitcoin['close'].iloc[-1] > bitcoin['Moving_Avg'].iloc[-1]: return True
    else: return False

def GO_SHORT_CONDITION(dataset, bitcoin):
    if (dataset['close'].iloc[-1] < dataset['close'].iloc[-2] and dataset['close'].iloc[-1] < dataset['close'].iloc[-3]) and \
        bitcoin['close'].iloc[-1] < bitcoin['Moving_Avg'].iloc[-1]: return True
    else: return False

def EXIT_LONG_CONDITION(dataset, bitcoin):
    if (dataset['close'].iloc[-1] < dataset['close'].iloc[-2] and dataset['close'].iloc[-1] < dataset['close'].iloc[-3]) or \
        bitcoin['close'].iloc[-1] < bitcoin['Moving_Avg'].iloc[-1]: return True
    else: return False

def EXIT_SHORT_CONDITION(dataset, bitcoin):
    if (dataset['close'].iloc[-1] > dataset['close'].iloc[-2] and dataset['close'].iloc[-1] > dataset['close'].iloc[-3]) or \
        bitcoin['close'].iloc[-1] > bitcoin['Moving_Avg'].iloc[-1]: return True
    else: return False

def test():
    klines = klines_4HOUR(0)
    bitcoin = Moving_Average_of_Bitcoin()

    long = GO_LONG_CONDITION(klines, bitcoin)
    print("Long: " + str(long))

    short = GO_SHORT_CONDITION(klines, bitcoin)
    print("Short: " + str(short))

# test()