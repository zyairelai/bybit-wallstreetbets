import config
import strategy
import pandas, os
from datetime import datetime

strategy = strategy
fees = 0.2

def backtest():
    all_pairs = 0
    for i in range(len(config.pair)):
        pair     = config.pair[i]
        leverage = config.leverage[i]
        real_dataset = strategy.swing_trade(pair)[["timestamp", "high", "low", "close", "volume", "volumeAvg", "GO_LONG", "GO_SHORT"]].copy()
        print(real_dataset)

        feda_klines = "feda_output.json"
        test_dataset = pandas.read_json(feda_klines).rename({0: 'timestamp', 1: 'o', 2: 'h', 3: 'l', 4: 'c', 5: 'v'}, axis=1) 
        mixed_dataset = pandas.merge_asof(test_dataset, real_dataset, on='timestamp')
        mixed_dataset.drop('o', axis=1, inplace=True)
        print(mixed_dataset)

        print("\n\n" + pair)
        print("Start Time Since " + str(datetime.fromtimestamp(mixed_dataset["timestamp"].iloc[0]/1000)))

        long_result = round(check_PNL(mixed_dataset, real_dataset, leverage, "_LONG"), 2)
        short_reult = round(check_PNL(mixed_dataset, real_dataset, leverage, "SHORT"), 2)
        overall_result = round(long_result + short_reult, 2)
        all_pairs = round(all_pairs + overall_result, 2)

        print("PNL for _BOTH Positions: " + str(overall_result) + "%\n")
    print("ALL PAIRS PNL : " + str(all_pairs) + "%\n")
    os.remove(feda_klines)


def check_PNL(mixed_dataset, real_dataset, leverage, positionSide):
    position = False
    cumulative_volume = 0
    total_pnl, total_trades = 0, 0
    wintrade, losetrade = 0, 0

    if positionSide == "_LONG":
        open_position = "GO_LONG"
        entry_indicat = "high"
        liq_indicator = "low"

    elif positionSide == "SHORT":
        open_position = "GO_SHORT"
        entry_indicat = "low"
        liq_indicator = "high"

    for index in range(len(mixed_dataset)):

        if mixed_dataset['timestamp'].iloc[index] in real_dataset['timestamp'].values:
            cumulative_volume = 0
        else: cumulative_volume = cumulative_volume + mixed_dataset['v']

        if not position:
            if mixed_dataset[open_position].iloc[index] and cumulative_volume > mixed_dataset['volumeAvg']:
                position = True
                entry_price = mixed_dataset["c"].iloc[index]
                current_low = mixed_dataset["c"].iloc[index]
                current_high = mixed_dataset["c"].iloc[index]
        else:
            trailing_stop = (mixed_dataset[liq_indicator].iloc[index] - entry_indicat) / entry_indicat * 100 * leverage < -leverage
            if trailing_stop:
                position = False
                realized_pnl = ((mixed_dataset["close"].iloc[index] - entry_price) / entry_price * 100 * leverage) - (fees * leverage)

                if realized_pnl > 0: wintrade = wintrade + 1
                else: losetrade = losetrade + 1

                total_trades = total_trades + 1
                total_pnl = total_pnl + realized_pnl

    if total_pnl != 0:
        print("PNL for " + positionSide + " Positions: " + str(round(total_pnl, 2)) + "%")
        print("Total  Executed  Trades: " + str(round(total_trades, 2)))
        print("_Win Trades: " + str(wintrade))
        print("Lose Trades: " + str(losetrade))
        if (wintrade + losetrade > 1):
            winrate = round(wintrade / (wintrade + losetrade) * 100)
            print("Winrate : " + str(winrate) + " %")
        print()

    return round(total_pnl, 2)

backtest()