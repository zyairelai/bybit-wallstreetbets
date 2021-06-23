live_trade = False
enable_scheduler = False

coin     = ["BTC", "ETH"]
quantity = [0.001, 0.01]
leverage = [30, 20]

# Recommended Leverage
# if   markPrice[i] < 1: leverage.append(5)
# elif markPrice[i] < 10: leverage.append(10)
# elif markPrice[i] < 100: leverage.append(15)
# elif markPrice[i] < 1000: leverage.append(20)
# elif markPrice[i] < 10000: leverage.append(25)
# elif markPrice[i] < 100000: leverage.append(30)