live_trade = False

coin = ["BTC", "ETH", "BNB", "BCH", "LTC"]
quantity = [0.001, 0.01, 0.02, 0.02, 0.05]

leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(15)
    elif coin[i] == "ETH": leverage.append(10)
    else: leverage.append(5)
