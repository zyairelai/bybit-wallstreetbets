live_trade = False

use_trailing = True
callbackrate = 4

coin = ["BTC", "ETH", "BNB", "LTC"]
quantity = [0.001, 0.01, 0.05, 0.1]

leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if coin[i] == "BTC" : leverage.append(15)
    elif coin[i] == "ETH" : leverage.append(15)
    else: leverage.append(10)
