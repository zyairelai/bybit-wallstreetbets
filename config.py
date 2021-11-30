live_trade = False
enable_scheduler = True
follow_bitcoin = True

use_trailing = True
callbackrate = 5

coin = ["BTC", "ETH", "BNB", "LTC"] # , "BCH", "XRP", "EOS", "TRX", "ADA", "IOTA", "DOGE", "LINK", "AXS", "ALICE"]
quantity = [0.001, 0.01, 0.05, 0.1]

pair, leverage = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if coin == "BTC": leverage.append(50)
    elif coin == "ETH": leverage.append(40)
    else: leverage.append(30)
