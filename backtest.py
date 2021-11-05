import config
import get_klines
from datetime import datetime

import strategy
strategy = strategy

fees = 0.2
entry_exit_indicator = 'close'

def backtest():
    all_pairs = 0
    for i in range(len(config.pair)):
        pair = config.pair[i]
        leverage = config.leverage[i]

        klines = get_klines.get_klines(pair)
        swing_trades = strategy.swing_trade(i, klines)
        # print(swing_trades)

        print("\n\n" + pair)
        print("Start Time Since " + str(datetime.fromtimestamp(swing_trades["timestamp"].iloc[0]/1000)))
        long_result = round(check_PNL(swing_trades, leverage, "_LONG"), 2)
        short_reult = round(check_PNL(swing_trades, leverage, "SHORT"), 2)
        overall_result = round(long_result + short_reult, 2)
        all_pairs = round(all_pairs + overall_result, 2)

        print("PNL for _BOTH Positions: " + str(overall_result) + "%\n")
    print("ALL PAIRS PNL : " + str(all_pairs) + "%\n")

def check_PNL(swing_trades, leverage, positionSide):
    position = False
    total_pnl, total_trades, total_liq = 0, 0, 0
    wintrade, losetrade = 0, 0

    if positionSide == "_LONG":
        open_position = "GO_LONG"
        exit_position = "EXIT_LONG"
        liq_indicator = "low"

    elif positionSide == "SHORT":
        open_position = "GO_SHORT"
        exit_position = "EXIT_SHORT"
        liq_indicator = "high"

    for index in range(len(swing_trades)):
        if not position:
            if swing_trades[open_position].iloc[index]:
                position = True
                entry_price = swing_trades[entry_exit_indicator].iloc[index]
        else:
            liquidation = (swing_trades[liq_indicator].iloc[index] - entry_price) / entry_price * 100 * leverage < -80
            if swing_trades[exit_position].iloc[index] or liquidation:
                position = False
                if liquidation:
                    realized_pnl = -100
                    total_liq = total_liq + 1
                else : realized_pnl = ((swing_trades[entry_exit_indicator].iloc[index] - entry_price) / entry_price * 100 * leverage) - (fees * leverage)

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