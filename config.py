live_trade = False
enable_scheduler = True
follow_bitcoin = True

use_trailing = True
callbackrate = 5

coin = ["BTC", "ETH", "BNB", "LTC"] # , "BCH", "XRP", "EOS", "TRX", "ADA", "IOTA", "DOGE", "LINK", "AXS", "ALICE"]
quantity = [0.001, 0.01, 0.05, 0.1]
leverage = 20

pair = []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
