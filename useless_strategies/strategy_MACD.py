def swing_trade(i, dataset):
    dataset['12_EMA'] = dataset['close'].ewm(span=12).mean()
    dataset['26_EMA'] = dataset['close'].ewm(span=26).mean()
    dataset['MACD'] = dataset['12_EMA'] - dataset['26_EMA']
    dataset['Signal'] = dataset['MACD'].ewm(span=9).mean()
    dataset['Histogram'] = dataset['MACD'] - dataset['Signal']

    dataset['GO_LONG'] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset['GO_SHORT'] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    dataset['EXIT_LONG'] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset['EXIT_SHORT'] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    clean = dataset.drop(['12_EMA', '26_EMA'], axis=1)
    # print(clean)
    return clean

def GO_LONG_CONDITION(dataset):
    if  dataset['Signal'] < 0 and \
        dataset['Signal'] < dataset['MACD'] and \
        dataset['Histogram'] > 0 : return True 
    else: return False

def GO_SHORT_CONDITION(dataset):
    if  dataset['Signal'] > 0 and \
        dataset['Signal'] > dataset['MACD'] and \
        dataset['Histogram'] < 0 : return True  
    else: return False

def EXIT_LONG_CONDITION(dataset):
    return True if dataset['Histogram'] < 0 else False

def EXIT_SHORT_CONDITION(dataset):
    return True if dataset['Histogram'] > 0 else False
