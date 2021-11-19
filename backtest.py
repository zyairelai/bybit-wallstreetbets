import config
import strategy
from datetime import datetime

fees = 0.2
use_trailing = True

def backtest():
    all_pairs = 0
    for i in range(len(config.pair)):
        print(config.pair[i])
        leverage = config.leverage[i]
        hero = strategy.swing_trade(config.pair[i])
        # print(hero)

        print("Start Time Since " + str(datetime.fromtimestamp(hero["timestamp"].iloc[0]/1000)))
        long_result = round(check_PNL(hero, leverage, "_LONG"), 2)
        short_reult = round(check_PNL(hero, leverage, "SHORT"), 2)
        overall_result = round(long_result + short_reult, 2)
        all_pairs = round(all_pairs + overall_result, 2)

        print("PNL for _BOTH Positions: " + str(overall_result) + "%\n")
    print("ALL PAIRS PNL : " + str(all_pairs) + "%\n")

def check_PNL(hero, leverage, positionSide):
    position = False
    total_pnl, total_trades, liquidations = 0, 0, 0
    wintrade, losetrade = 0, 0

    if positionSide == "_LONG":
        open_position = "GO_LONG"
        exit_position = "EXIT_LONG"
        liq_indicator = "low"

    elif positionSide == "SHORT":
        open_position = "GO_SHORT"
        exit_position = "EXIT_SHORT"
        liq_indicator = "high"

    for i in range(len(hero)):
        if not position:
            if hero[open_position].iloc[i]:
                entry_price = hero['open'].iloc[i]
                position = True
        else:
            if use_trailing:
                trailing_stop = (hero[liq_indicator].iloc[i] - entry_price) / entry_price * 100 * leverage < -(leverage * config.callbackrate)
            else:
                trailing_stop = (hero[liq_indicator].iloc[i] - entry_price) / entry_price * 100 * leverage < -80
            unrealizedPNL = (hero['open'].iloc[i] - entry_price) / entry_price * 100 * leverage
            breakeven_PNL = fees * leverage

            if (hero[exit_position].iloc[i]) or trailing_stop:
                if trailing_stop:
                    if use_trailing: realized_pnl = -breakeven_PNL - (leverage * config.callbackrate)
                    else: realized_pnl = -100 
                    liquidations = liquidations + 1
                else: realized_pnl = unrealizedPNL - breakeven_PNL

                if realized_pnl > 0: wintrade = wintrade + 1
                else: losetrade = losetrade + 1

                total_trades = total_trades + 1
                total_pnl = total_pnl + realized_pnl
                position = False

    if total_pnl != 0:
        print("PNL for " + positionSide + " Positions: " + str(round(total_pnl, 2)) + "%")
        print("Total  Executed  Trades: " + str(round(total_trades, 2)))
        print("Triggered Trailing Stop: " + str(round(liquidations)))
        print("_Win Trades: " + str(wintrade))
        print("Lose Trades: " + str(losetrade))
        if (wintrade + losetrade > 1):
            winrate = round(wintrade / (wintrade + losetrade) * 100)
            print("Winrate : " + str(winrate) + " %")
        print()

    return round(total_pnl, 2)

backtest()