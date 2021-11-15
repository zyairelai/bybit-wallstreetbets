import pandas
import modules.candlestick
import modules.heikin_ashi

test_module = True

def swing_trade(pair):
    # Fetch the raw klines data
    main_raw = modules.candlestick.get_klines(pair, '6h')
    support  = modules.candlestick.get_klines(pair, '1h')

    # Process Heikin Ashi & Apply Technical Analysis
    main_candle = modules.candlestick.candlestick(main_raw)[["timestamp", "open", "high", "low", "close", "volume", "volumeAvg"]].copy()
    ha_6_hours  = modules.heikin_ashi.heikin_ashi(main_raw)[["timestamp", "candle"]].copy()
    ha_6_hours  = ha_6_hours.rename(columns={'candle': 'HA_6hour'})
    ha_1_hours  = modules.heikin_ashi.heikin_ashi(support)[["timestamp", "candle"]].copy()
    ha_1_hours  = ha_1_hours.rename(columns={'candle': 'HA_1hour'})

    dataset = pandas.merge_asof(main_candle, ha_6_hours, on='timestamp')
    dataset = pandas.merge_asof(ha_1_hours, dataset, on='timestamp')

    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    return dataset

def GO_LONG_CONDITION(klines):
    color = "GREEN"
    if  klines['HA_6hour'] == color and \
        klines['HA_1hour'] == color and \
        klines['volume'] > klines["volumeAvg"]: return True
    else: return False

def GO_SHORT_CONDITION(klines):
    color = "RED"
    if  klines['HA_6hour'] == color and \
        klines['HA_1hour'] == color and \
        klines['volume'] > klines["volumeAvg"]: return True
    else: return False

if test_module:
    run = swing_trade(("ETH" + "USDT").upper())
    print(run)
