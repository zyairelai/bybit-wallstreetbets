live_trade = False
enable_scheduler = False

coin = ["BTC", "ETH", "BNB", "BCH", "LTC", "XRP"]

# coin     = ["BTC", "ETH"]
quantity = [0.001, 0.01]

leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(30)
    elif coin[i] == "ETH": leverage.append(20)
    else: leverage.append(10)
