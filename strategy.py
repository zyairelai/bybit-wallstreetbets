import config, ccxt, pandas
ccxt_client = ccxt.binance()

query = 100
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

def klines_4HOUR(i):
    print(config.pair[i])
    klines = pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '4h', limit=query), columns=tohlcv_column)
    klines['color'] = klines.apply(candle_color, axis=1)
    return klines

def candle_color(klines):
    if klines['open'] > klines['close']: return "RED"
    elif klines['open'] < klines['close']: return "GREEN"
    else: return "INDECISIVE"

def Moving_Average_of_Bitcoin():
    bitcoin = pandas.DataFrame(ccxt_client.fetch_ohlcv("BTC/USDT", '1d', limit=query), columns=tohlcv_column)
    bitcoin['Moving_Avg'] = bitcoin["close"].rolling(window=50).mean()
    bitcoin = bitcoin.drop(['volume'], axis=1)
    return bitcoin

def GO_LONG_CONDITION(dataset):
    if (dataset['close'].iloc[-1] > dataset['close'].iloc[-2] and dataset['close'].iloc[-1] > dataset['close'].iloc[-3]) and \
        dataset['close'].iloc[-1] > Moving_Average_of_Bitcoin()['Moving_Avg'].iloc[-1]: return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    if (dataset['close'].iloc[-1] < dataset['close'].iloc[-2] and dataset['close'].iloc[-1] < dataset['close'].iloc[-3]) and \
        dataset['close'].iloc[-1] < Moving_Average_of_Bitcoin()['Moving_Avg'].iloc[-1]: return True
    else: return False

def EXIT_LONG_CONDITION(dataset):
    if (dataset['close'].iloc[-1] < dataset['close'].iloc[-2] and dataset['close'].iloc[-1] < dataset['close'].iloc[-3]) and \
        dataset['close'].iloc[-1] < Moving_Average_of_Bitcoin()['Moving_Avg'].iloc[-1]: return True
    else: return False

def EXIT_SHORT_CONDITION(dataset):
    if (dataset['close'].iloc[-1] > dataset['close'].iloc[-2] and dataset['close'].iloc[-1] > dataset['close'].iloc[-3]) and \
        dataset['close'].iloc[-1] > Moving_Average_of_Bitcoin()['Moving_Avg'].iloc[-1]: return True
    else: return False
