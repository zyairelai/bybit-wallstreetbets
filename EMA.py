def compute(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def current(EMA_list) : return EMA_list[-1]
def previous(EMA_list): return EMA_list[-2]

def GOING_UP(EMA_list):
    if current(EMA_list) > previous(EMA_list): return True

def GOING_DOWN(EMA_list):
    if current(EMA_list) < previous(EMA_list): return True

def UP_TREND(low, high):
    if current(low) > current(high): return True

def DOWN_TREND(low, high):
    if current(high) > current(low): return True

def BOTH_GOING_UP(low, high):
    if GOING_UP(low) and GOING_UP(high): return True

def BOTH_GOING_DOWN(low, high):
    if GOING_DOWN(low) and GOING_DOWN(high): return True

def ALL_GOING_UP(low, high):
    if UP_TREND(low, high) and BOTH_GOING_UP(low, high): return True

def ALL_GOING_DOWN(low, high):
    if DOWN_TREND(low, high) and BOTH_GOING_DOWN(low, high): return True

def DELTA_UP(low, medium, high):
    if current(low) > current(medium) and current(medium) > current(high): return True

def DELTA_DOWN(low, medium, high):
    if current(high) > current(medium) and current(medium) > current(low): return True
