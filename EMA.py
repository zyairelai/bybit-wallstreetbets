def compute(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def current(EMA_list) : return float(EMA_list[-1])
def previous(EMA_list): return float(EMA_list[-2])

def UPWARD_MOVEMENT(EMA_list):
    if current(EMA_list) > previous(EMA_list): return True

def DOWNWARD_MOVEMENT(EMA_list):
    if current(EMA_list) < previous(EMA_list): return True

def BOTH_GOING_UP(low, high):
    if UPWARD_MOVEMENT(low) and UPWARD_MOVEMENT(high): return True

def BOTH_GOING_DOWN(low, high):
    if DOWNWARD_MOVEMENT(low) and DOWNWARD_MOVEMENT(high): return True

def DELTA_UP(low, medium, high):
    if current(low) > current(medium) and UPWARD_MOVEMENT(high): return True

def DELTA_DOWN(low, medium, high):
    if current(medium) > current(low) and DOWNWARD_MOVEMENT(high): return True
