def current(EMA_list):
    return EMA_list[-1]

def previous(EMA_list):
    return EMA_list[-2]

def compute(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def GOING_UP(current_ema_low, current_ema_high):
    if current_ema_low > current_ema_high: return True

def GOING_DOWN(current_ema_low, current_ema_high):
    if current_ema_low < current_ema_high: return True
