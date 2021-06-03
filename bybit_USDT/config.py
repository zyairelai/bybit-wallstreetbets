live_trade = False
enable_scheduler = False

lower_EMA  = 3
higher_EMA = 7

coin     = ["BTC"]
quantity = [0.001]
leverage = 20

pair = []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage))
    print()
