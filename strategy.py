import pandas
import modules.candlestick
import modules.heikin_ashi

test_module = False

def swing_trade(pair):
    # Fetch the raw klines data
    get_raw = modules.candlestick.get_klines(pair, '1h')

    # Process Heikin Ashi & Apply Technical Analysis
    candlestick = modules.candlestick.candlestick(get_raw)[["timestamp", "open", "high", "low", "close", "volume", "volumeAvg", "color"]].copy()
    heikin_ashi = modules.heikin_ashi.heikin_ashi(get_raw)[["timestamp", "candle"]].copy()
    candlestick = candlestick.rename(columns={'color': 'candlestick'})
    heikin_ashi = heikin_ashi.rename(columns={'candle': 'heikin_ashi'})
    
    dataset = pandas.merge_asof(candlestick, heikin_ashi, on='timestamp')
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    return dataset

def GO_LONG_CONDITION(klines):
    color = "GREEN"
    if  klines['candlestick'] == color and \
        klines['heikin_ashi'] == color and \
        klines['volume'] > klines["volumeAvg"]: return True
    else: return False

def GO_SHORT_CONDITION(klines):
    color = "RED"
    if  klines['candlestick'] == color and \
        klines['heikin_ashi'] == color and \
        klines['volume'] > klines["volumeAvg"]: return True
    else: return False

if test_module:
    run = swing_trade(("ETH" + "USDT").upper())
    print(run)
