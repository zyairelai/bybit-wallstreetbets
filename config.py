live_trade = False
enable_scheduler = False

coin = ["BTC", "ETH", "BNB", "BCH", "LTC"]
quantity = [0.001, 0.01, 0.05, 0.05, 0.15]

leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(40)
    elif coin[i] == "ETH": leverage.append(30)
    else: leverage.append(20)
