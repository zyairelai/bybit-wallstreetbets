live_trade = True
enable_scheduler = False

lower_EMA  = 3
higher_EMA = 7

coin     = ["IOTA", "KAVA", "KNC"] # "1INCH", "ETC", "CRV"
quantity = [15, 4, 8]
leverage = 20

pair = []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage))
    print()
