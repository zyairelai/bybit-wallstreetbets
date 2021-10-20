live_trade = False
enable_scheduler = False

coin     = ["BTC"]
quantity = [0.001]

leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(20)
    elif coin[i] == "ETH": leverage.append(15)
    else: leverage.append(10)
