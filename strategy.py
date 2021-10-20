import config, ccxt, pandas
ccxt_client = ccxt.binance()
current, previous, query = -1, -2, 54
tohlcv_column = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

def dataset(i):
    print(config.pair[i])
    klines = pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '4h', limit=query), columns=tohlcv_column)
    klines["color"] = klines.apply(candle_color, axis=1)
    
    GO_LONG_CONDITION(klines)
    print(klines)

def candle_color(klines):
    if klines['open'] > klines['close']: return "RED"
    elif klines['open'] < klines['close']: return "GREEN"
    else: return "INDECISIVE"

def Moving_Average_of_Bitcoin():
    bitcoin = pandas.DataFrame(ccxt_client.fetch_ohlcv("BTC/USDT", '4h', limit=query), columns=tohlcv_column)
    bitcoin['Moving Average'] = bitcoin.iloc[:,1].rolling(window=50).mean()
    # print(bitcoin)
    return bitcoin

def GO_LONG_CONDITION(dataset):
    if (dataset['color'].iloc[current] == "GREEN" and dataset['color'].iloc[previous] == "GREEN" and dataset['color'].iloc[-3] == "GREEN") and \
        dataset['close'].iloc[current] > Moving_Average_of_Bitcoin()['Moving Average'].iloc[current]: return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    if (dataset['color'].iloc[current] == "RED" and dataset['color'].iloc[previous] == "RED" and dataset['color'].iloc[-3] == "RED") and \
        dataset['close'].iloc[current] < Moving_Average_of_Bitcoin()['Moving Average'].iloc[current]: return True
    else: return False

def EXIT_LONG_CONDITION(dataset):
    if (dataset['color'].iloc[current] == "RED" and dataset['color'].iloc[previous] == "RED" and dataset['color'].iloc[-3] == "RED") or \
        dataset['close'].iloc[current] < Moving_Average_of_Bitcoin()['Moving Average'].iloc[current]: return True
    else: return False

def EXIT_SHORT_CONDITION(dataset):
    if (dataset['color'].iloc[current] == "GREEN" and dataset['color'].iloc[previous] == "GREEN" and dataset['color'].iloc[-3] == "GREEN") or \
        dataset['close'].iloc[current] > Moving_Average_of_Bitcoin()['Moving Average'].iloc[current]: return True
    else: return False

dataset(0)
# Moving_Average_of_Bitcoin()
