def compute(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def current(EMA_list) : return float(EMA_list[-1])
def previous(EMA_list): return float(EMA_list[-2])

def UPTREND_ZONE(low, mid):
    if current(low) > current(mid): return True

def DOWNTREND_ZONE(low, mid):
    if current(mid) > current(low): return True

def UPWARD_MOVEMENT(EMA_list):
    if current(EMA_list) > previous(EMA_list): return True

def DOWNWARD_MOVEMENT(EMA_list):
    if current(EMA_list) < previous(EMA_list): return True

def DELTA_UP(low, mid, high):
    if UPTREND_ZONE(low, mid) and UPWARD_MOVEMENT(high): return True

def DELTA_DOWN(low, mid, high):
    if DOWNTREND_ZONE(low, mid) and DOWNWARD_MOVEMENT(high): return True
