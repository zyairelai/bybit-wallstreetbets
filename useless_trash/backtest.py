import feda
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
        long_term_low_leverage = strategy.swing_trade(pair)[["timestamp", "high", "low", "close", "volume", "volumeAvg", "GO_LONG", "GO_SHORT"]].copy()
        print(long_term_low_leverage)

        feda_klines = "feda_output.json"
        test_data = pandas.read_json(feda_klines).rename({0: 'timestamp', 1: 'o', 2: 'h', 3: 'l', 4: 'c', 5: 'v'}, axis=1) 
        dataset = pandas.merge_asof(test_data, long_term_low_leverage, on='timestamp')
        dataset.drop('o', axis=1, inplace=True)
        print(dataset)

        print("\n\n" + pair)
        print("Start Time Since " + str(datetime.fromtimestamp(long_term_low_leverage["timestamp"].iloc[0]/1000)))

    #     long_result = round(check_PNL(long_term_low_leverage, leverage, "_LONG"), 2)
    #     short_reult = round(check_PNL(long_term_low_leverage, leverage, "SHORT"), 2)
    #     overall_result = round(long_result + short_reult, 2)
    #     all_pairs = round(all_pairs + overall_result, 2)

    #     print("PNL for _BOTH Positions: " + str(overall_result) + "%\n")
    # print("ALL PAIRS PNL : " + str(all_pairs) + "%\n")
    os.remove(feda_klines)


def check_PNL(swing_trades, leverage, positionSide):

    position = False
    total_pnl, total_trades, total_liq = 0, 0, 0
    wintrade, losetrade = 0, 0

    if positionSide == "_LONG":
        open_position = "GO_LONG"
        entry_indicat = "high"
        liq_indicator = "low"

    elif positionSide == "SHORT":
        open_position = "GO_SHORT"
        entry_indicat = "low"
        liq_indicator = "high"

    for index in range(len(swing_trades)):
        if not position:
            if swing_trades[open_position].iloc[index]:
                position = True
                entry_price = swing_trades["close"].iloc[index]
        else:
            trailing_stop = (swing_trades[liq_indicator].iloc[index] - entry_indicat) / entry_indicat * 100 * leverage < -leverage
            if swing_trades[exit_position].iloc[index] or liquidation:
                position = False
                if liquidation:
                    realized_pnl = -100
                    total_liq = total_liq + 1
                else : realized_pnl = ((swing_trades["close"].iloc[index] - entry_price) / entry_price * 100 * leverage) - (fees * leverage)

                if realized_pnl > 0: wintrade = wintrade + 1
                else: losetrade = losetrade + 1

                total_trades = total_trades + 1
                total_pnl = total_pnl + realized_pnl

    if total_pnl != 0:
        print("PNL for " + positionSide + " Positions: " + str(round(total_pnl, 2)) + "%")
        print("Total  Executed  Trades: " + str(round(total_trades, 2)))
        print("Total Liquidated Trades: " + str(round(total_liq)))
        print("_Win Trades: " + str(wintrade))
        print("Lose Trades: " + str(losetrade))
        if (wintrade + losetrade > 1):
            winrate = round(wintrade / (wintrade + losetrade) * 100)
            print("Winrate : " + str(winrate) + " %")
        print()

    return round(total_pnl, 2)

backtest()