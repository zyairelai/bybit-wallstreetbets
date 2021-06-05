def compute(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def current(EMA_list) : return EMA_list[-1]
def previous(EMA_list): return EMA_list[-2]

def UP_TREND(low, high):
    if current(low) > current(high): return True

def DOWN_TREND(low, high):
    if current(high) > current(low): return True

def GOING_UP(EMA_list):
    if current(EMA_list) > previous(EMA_list): return True

def GOING_DOWN(EMA_list):
    if current(EMA_list) < previous(EMA_list): return True
