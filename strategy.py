import candlestick

indicator = "open"
test_module = False

def long_term_low_leverage(pair):
    wanted_column = ["timestamp", "open", "high", "low", "close", "volume", "GO_LONG", "GO_SHORT", "EXIT_LONG", "EXIT_SHORT"]
    dataset = create_dataset(pair)[wanted_column].copy()
    # bitcoin = create_dataset("BTCUSDT")[wanted_column].copy()
    return dataset

def create_dataset(pair):
    dataset = candlestick.get_klines(pair, '1d')

    # Temporary Previous 7 days HIGH
    dataset["high_1"] = dataset['high'].shift(1)
    dataset["high_2"] = dataset['high'].shift(2)
    dataset["high_3"] = dataset['high'].shift(3)
    dataset["high_4"] = dataset['high'].shift(4)
    dataset["high_5"] = dataset['high'].shift(5)
    dataset["high_6"] = dataset['high'].shift(6)
    dataset["high_7"] = dataset['high'].shift(7)
    dataset["high_8"] = dataset['high'].shift(8)

    # Temporary Previous 7 days LOW
    dataset["low_1"] = dataset['low'].shift(1)
    dataset["low_2"] = dataset['low'].shift(2)
    dataset["low_3"] = dataset['low'].shift(3)
    dataset["low_4"] = dataset['low'].shift(4)
    dataset["low_5"] = dataset['low'].shift(5)
    dataset["low_6"] = dataset['low'].shift(6)
    dataset["low_7"] = dataset['low'].shift(7)
    dataset["low_8"] = dataset['low'].shift(8)

    # Moving Average but actually useless
    # moving_average_threshold = 200
    # dataset['SMA'] = dataset['close'].rolling(window=moving_average_threshold).mean()
    # dataset['EMA'] = dataset['close'].ewm(span=moving_average_threshold).mean()

    # Apply Place Order Condition
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    dataset["EXIT_LONG"] = dataset.apply(EXIT_LONG_CONDITION, axis=1)
    dataset["EXIT_SHORT"] = dataset.apply(EXIT_SHORT_CONDITION, axis=1)
    dataset = dataset.dropna()
    return dataset

def GO_LONG_CONDITION(dataset):
    if  dataset[indicator] < dataset["low_8"] and \
        dataset[indicator] < dataset["low_2"] and \
        dataset[indicator] < dataset["low_3"] and \
        dataset[indicator] < dataset["low_4"] and \
        dataset[indicator] < dataset["low_5"] and \
        dataset[indicator] < dataset["low_6"] and \
        dataset[indicator] < dataset["low_7"]: return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    if  dataset[indicator] > dataset["high_8"] and \
        dataset[indicator] > dataset["high_2"] and \
        dataset[indicator] > dataset["high_3"] and \
        dataset[indicator] > dataset["high_4"] and \
        dataset[indicator] > dataset["high_5"] and \
        dataset[indicator] > dataset["high_6"] and \
        dataset[indicator] > dataset["high_7"]: return True
    else: return False

def EXIT_LONG_CONDITION(dataset):
    if  dataset[indicator] > dataset["high_8"] and \
        dataset[indicator] > dataset["high_2"] and \
        dataset[indicator] > dataset["high_3"] and \
        dataset[indicator] > dataset["high_4"] and \
        dataset[indicator] > dataset["high_5"] and \
        dataset[indicator] > dataset["high_6"] and \
        dataset[indicator] > dataset["high_7"] : return True
    else: return False

def EXIT_SHORT_CONDITION(dataset):
    if  dataset[indicator] < dataset["low_8"] and \
        dataset[indicator] < dataset["low_2"] and \
        dataset[indicator] < dataset["low_3"] and \
        dataset[indicator] < dataset["low_4"] and \
        dataset[indicator] < dataset["low_5"] and \
        dataset[indicator] < dataset["low_6"] and \
        dataset[indicator] < dataset["low_7"] : return True
    else: return False

if test_module:
    swing_trade = long_term_low_leverage("BTCUSDT")
    print(swing_trade)
