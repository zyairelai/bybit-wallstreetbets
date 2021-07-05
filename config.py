live_trade = True
enable_scheduler = False

coin     = ["BTC"]
quantity = [0.001]

def set_Defaut_Leverage(markPrice):
    if   markPrice < 1: leverage = 5
    elif markPrice < 10: leverage = 10
    elif markPrice < 100: leverage = 15
    elif markPrice < 1000: leverage = 20
    elif markPrice < 10000: leverage = 25
    else: leverage = 30
    return int(leverage)
