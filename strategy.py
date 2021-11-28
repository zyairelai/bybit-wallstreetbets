import candlestick, config

indicator = "open"
test_module = False

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

    # Apply Place Order Condition
    dataset["BUY"] = dataset.apply(BUY_CONDITION, axis=1)
    dataset["SELL"] = dataset.apply(SELL_CONDITION, axis=1)
    dataset = dataset.dropna()
    return dataset

def long_term_low_leverage(pair):
    dataset = create_dataset(pair)[["timestamp", "open", "high", "low", "close", "volume", "BUY", "SELL"]].copy()

    if config.follow_bitcoin:
        buy, sell = [], []
        bitcoin = create_dataset("BTCUSDT")[["BUY", "SELL"]].copy()
        bitcoin = bitcoin.rename(columns={'BUY': 'BUY_BTC'})
        bitcoin = bitcoin.rename(columns={'SELL': 'SELL_BTC'})
        dataset = dataset.rename(columns={'BUY': 'BUY_PAIR'})
        dataset = dataset.rename(columns={'SELL': 'SELL_PAIR'})

        # ethereum = create_dataset("ETHUSDT")[["BUY", "SELL"]].copy()
        # ethereum = ethereum.rename(columns={'BUY': 'BUY_ETH'})
        # ethereum = ethereum.rename(columns={'SELL': 'SELL_ETH'})

        for i in range(len(dataset)):
            buy.append(dataset["BUY_PAIR"].iloc[i] or bitcoin["BUY_BTC"].iloc[i])
            sell.append(dataset["SELL_PAIR"].iloc[i] or bitcoin["SELL_BTC"].iloc[i])
            # buy.append(dataset["BUY_PAIR"].iloc[i] or bitcoin["BUY_BTC"].iloc[i] or ethereum["BUY_ETH"].iloc[i])
            # sell.append(dataset["SELL_PAIR"].iloc[i] or bitcoin["SELL_BTC"].iloc[i] or ethereum["SELL_ETH"].iloc[i])

        dataset["BUY_BTC"] = bitcoin["BUY_BTC"]
        dataset["SELL_BTC"] = bitcoin["SELL_BTC"]
        dataset["BUY"] = buy
        dataset["SELL"] = sell

    return dataset

def BUY_CONDITION(dataset):
    if  dataset[indicator] < dataset["low_8"] and \
        dataset[indicator] < dataset["low_2"] and \
        dataset[indicator] < dataset["low_3"] and \
        dataset[indicator] < dataset["low_4"] and \
        dataset[indicator] < dataset["low_5"] and \
        dataset[indicator] < dataset["low_6"] and \
        dataset[indicator] < dataset["low_7"]: return True
    else: return False

def SELL_CONDITION(dataset):
    if  dataset[indicator] > dataset["high_8"] and \
        dataset[indicator] > dataset["high_2"] and \
        dataset[indicator] > dataset["high_3"] and \
        dataset[indicator] > dataset["high_4"] and \
        dataset[indicator] > dataset["high_5"] and \
        dataset[indicator] > dataset["high_6"] and \
        dataset[indicator] > dataset["high_7"]: return True
    else: return False

if test_module:
    swing_trade = long_term_low_leverage("BTCUSDT")
    print(swing_trade)
