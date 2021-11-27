import config
import pandas
import strategy
from datetime import datetime

fees = 0.2

def backtest():
    all_pairs = 0
    long_pnl_data, short_pnl_data, overall, single_row_data = [], [], [], []

    for i in range(len(config.pair)):
        pair = config.pair[i]
        leverage = config.leverage[i]
        hero = strategy.long_term_low_leverage(pair)
        # print(hero)

        long_pnl_data.append(check_PNL(pair, hero, leverage, "LONG"))
        short_pnl_data.append(check_PNL(pair, hero, leverage, "SHORT"))

        single_row_data = [(long_pnl_data[i][0]),
                           (long_pnl_data[i][1] + short_pnl_data[i][1]),
                           (long_pnl_data[i][2] + short_pnl_data[i][2]),
                           (long_pnl_data[i][3] + short_pnl_data[i][3]),
                           ((long_pnl_data[i][4] + short_pnl_data[i][4]) / 2),
                           (long_pnl_data[i][5] + short_pnl_data[i][5])]
        overall.append(single_row_data)

    column_name = ["PAIR", "TRADES", "WINS", "LOSES", "WINRATE(%)", "PNL(%)"]
    long_column = pandas.DataFrame(long_pnl_data, columns = column_name)
    short_column = pandas.DataFrame(short_pnl_data, columns = column_name)
    overall = pandas.DataFrame(overall, columns = ["PAIR", "TRADES", "WINS", "LOSES", "WINRATE(%)", "PNL(%)"])
    print("\nStart Time Since " + str(datetime.fromtimestamp(hero["timestamp"].iloc[0]/1000)) + "\n")

    print("LONG POSITION")
    print(long_column)
    print("Avg WINRATE : " + str(round(long_column["WINRATE(%)"].sum() / len(config.pair), 2)) + "%")
    print("Total PNL   : " + str(round(long_column["PNL(%)"].sum(), 2)) + "%\n")
    
    print("SHORT POSITION")
    print(short_column)
    print("Avg WINRATE : " + str(round(short_column["WINRATE(%)"].sum() / len(config.pair), 2)) + "%")
    print("Total PNL : " + str(round(short_column["PNL(%)"].sum(), 2)) + "%\n")

    print("OVERALL INSIGHT")
    print(overall)
    print("Avg WINRATE : " + str(round(overall["WINRATE(%)"].sum() / len(config.pair), 2)) + "%")
    print("Total PNL : " + str(round(overall["PNL(%)"].sum(), 2)) + "%\n")

def check_PNL(pair, hero, leverage, positionSide):
    position = False
    total_pnl, total_trades, liquidations = 0, 0, 0
    wintrade, losetrade = 0, 0

    if positionSide == "LONG":
        open_position = "BUY"
        exit_position = "SELL"
        liq_indicator = "low"

    elif positionSide == "SHORT":
        open_position = "SELL"
        exit_position = "BUY"
        liq_indicator = "high"

    for i in range(len(hero)):
        if not position:
            if hero[open_position].iloc[i]:
                entry_price = hero['open'].iloc[i]
                position = True
        else:
            if config.use_trailing:
                trailing_stop = (hero[liq_indicator].iloc[i] - entry_price) / entry_price * 100 * leverage < -(leverage * config.callbackrate)
            else:
                trailing_stop = (hero[liq_indicator].iloc[i] - entry_price) / entry_price * 100 * leverage < -80
            unrealizedPNL = (hero['open'].iloc[i] - entry_price) / entry_price * 100 * leverage
            breakeven_PNL = fees * leverage

            if (hero[exit_position].iloc[i]) or trailing_stop:
                if trailing_stop:
                    if config.use_trailing: realized_pnl = -breakeven_PNL - (leverage * config.callbackrate)
                    else: realized_pnl = -100 
                    # liquidations = liquidations + 1
                else: realized_pnl = unrealizedPNL - breakeven_PNL

                if realized_pnl > 0: wintrade = wintrade + 1
                else: losetrade = losetrade + 1

                total_trades = total_trades + 1
                total_pnl = total_pnl + realized_pnl
                position = False

    pnl_info = []
    pnl_info.append(pair)
    pnl_info.append(round(total_trades, 2))
    # pnl_info.append(round(liquidations))
    pnl_info.append(wintrade)
    pnl_info.append(losetrade)

    if wintrade + losetrade > 0: pnl_info.append(round(wintrade / (wintrade + losetrade) * 100))
    else : pnl_info.append(0)

    pnl_info.append(round(total_pnl, 2))
    return pnl_info

backtest()