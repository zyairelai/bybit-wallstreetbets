import config
import strategy
import retrieve_klines
from datetime import datetime

fees = 0.2

def backtest():
    print("\n_Big_ Timeframe : " + retrieve_klines.big_timeframe)
    print("Entry Timeframe : " + retrieve_klines.entry_timeframe + "\n")

    all_pairs = 0
    for i in range(len(config.coin)):
        klines = retrieve_klines.retrieve_klines(i)
        swing_trades = strategy.swing_trade(i, klines)
        # print(swing_trades)

        print("\n\n" + config.pair[i])
        print("Start Time Since " + str(datetime.fromtimestamp(swing_trades["timestamp"].iloc[0]/1000)))
        long_result = round(check_for_long(i, swing_trades), 2)
        short_reult = round(check_for_short(i, swing_trades), 2)
        overall_result = round(long_result + short_reult, 2)
        all_pairs = round(all_pairs + overall_result, 2)

        print("PNL for _BOTH Positions: " + str(overall_result) + "%\n")
    print("ALL PAIRS PNL : " + str(all_pairs) + "%\n")

def check_for_long(i, swing_trades):
    position = False
    total_pnl, total_trades, total_liq = 0, 0, 0
    wintrade, losetrade = 0, 0

    for index in range(len(swing_trades)):
        if not position:
            if swing_trades["GO_LONG"].iloc[index]:
                position = True
                entry_price = swing_trades['open'].iloc[index]
        else:
            liquidation = (swing_trades['low'].iloc[index] - entry_price) / entry_price * 100 * config.leverage[i] < -80
            if swing_trades["EXIT_LONG"].iloc[index] or liquidation:
                position = False
                if liquidation:
                    realized_pnl = -100
                    total_liq = total_liq + 1
                else : realized_pnl = ((swing_trades['open'].iloc[index] - entry_price) / entry_price * 100 * config.leverage[i]) - (fees * config.leverage[i])
                
                if realized_pnl > 0.2 * config.leverage[i]: wintrade = wintrade + 1
                else: losetrade = losetrade + 1
                
                total_trades = total_trades + 1
                total_pnl = total_pnl + realized_pnl

    print("PNL for _Long Positions: " + str(round(total_pnl, 2)) + "%")
    print("Total  Executed  Trades: " + str(round(total_trades, 2)))
    print("Total Liquidated Trades: " + str(round(total_liq)))
    print("_Win Trades: " + str(wintrade))
    print("Lose Trades: " + str(losetrade))
    if (wintrade + losetrade > 1):
        winrate = round(wintrade / (wintrade + losetrade) * 100)
        print("Winrate : " + str(winrate) + " %")
    print()
    return round(total_pnl, 2)

def check_for_short(i, swing_trades):
    position = False
    total_pnl, total_trades, total_liq = 0, 0, 0
    wintrade, losetrade = 0, 0

    for index in range(len(swing_trades)):
        if not position:
            if swing_trades["GO_SHORT"].iloc[index]:
                position = True
                entry_price = swing_trades['open'].iloc[index]
        else:
            liquidation = (swing_trades['high'].iloc[index] - entry_price) / entry_price * 100 * config.leverage[i] < -80
            if swing_trades["EXIT_SHORT"].iloc[index] or liquidation:
                position = False
                if liquidation:
                    total_liq = total_liq + 1
                    realized_pnl = -100
                else: realized_pnl = ((swing_trades['open'].iloc[index] - entry_price) / entry_price * 100 * config.leverage[i]) - (fees * config.leverage[i])
                
                if realized_pnl > 0.2 * config.leverage[i]: wintrade = wintrade + 1
                else: losetrade = losetrade + 1
                
                total_trades = total_trades + 1
                total_pnl = total_pnl + realized_pnl

    print("PNL for Short Positions: " + str(round(total_pnl, 2)) + "%")
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