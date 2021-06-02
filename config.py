live_trade = True
enable_scheduler = False

lower_EMA  = 3
higher_EMA = 7

coin     = ["BNB", "DOGE", "IOTA"]
quantity = [0.05, 50, 15]
leverage = 20

pair = []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage))
    print()
