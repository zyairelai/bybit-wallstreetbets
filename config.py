live_trade = True
enable_scheduler = True
follow_bitcoin = True

use_trailing = False
callbackrate = 5

coin = ["BTC", "ETH"]#, "BNB", "LTC"] # , "BCH", "XRP", "EOS", "TRX", "ADA", "IOTA", "DOGE", "LINK", "AXS", "ALICE"]
quantity = [0.001, 0.01]#, 0.05, 0.1]

pair, leverage = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if coin[i] == "BTC": leverage.append(15)
    elif coin[i] == "ETH": leverage.append(15)
    else: leverage.append(15)
