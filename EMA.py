def compute(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def current(EMA_list) : return float(EMA_list[-1])
def previous(EMA_list): return float(EMA_list[-2])

def HIGHEST(low, mid, high):
    current_lines = [current(low), current(mid), current(high)]
    return max(current_lines)

def MIDDLE(low, mid, high):
    current_lines = [current(low), current(mid), current(high)]
    return sorted(current_lines)[1]

def LOWEST(low, mid, high):
    current_lines = [current(low), current(mid), current(high)]
    return min(current_lines)
