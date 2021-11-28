live_trade = False

follow_bitcoin = True
use_trailing = False
callbackrate = 4

coin = ["BTC", "ETH", "BNB", "LTC"] # , "BCH", "XRP", "EOS", "TRX", "ADA", "IOTA", "DOGE", "LINK", "AXS", "ALICE"]
quantity = [0.001, 0.01, 0.05, 0.1]

leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if use_trailing:
        if   callbackrate <= 1 : leverage.append(50)
        elif callbackrate <= 2 : leverage.append(40)
        elif callbackrate <= 3 : leverage.append(30)
        elif callbackrate <= 4 : leverage.append(20)
        elif callbackrate <= 5 : leverage.append(15)
    else: leverage.append(50)
