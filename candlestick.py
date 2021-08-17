from EMA import current


def previous_open(klines)   : return float(klines[-2].get('open'))
def previous_high(klines)   : return float(klines[-2].get('high'))
def previous_low(klines)    : return float(klines[-2].get('low'))
def previous_close(klines)  : return float(klines[-2].get('close'))
def previous_candle_body(klines) : return abs(previous_open(klines) - previous_close(klines))

def current_open(klines)    : return float(klines[-1].get('open'))
def current_close(klines)   : return float(klines[-1].get('close'))
def current_high(klines)    : return float(klines[-1].get('high'))
def current_low(klines)     : return float(klines[-1].get('low'))
def candle_body(klines)     : return abs(current_open(klines) - current_close(klines))
def candle_wick(klines)     : return current_high(klines) - current_low(klines) - candle_body(klines)

def price_decimal_place(klines):
    number = str(current_close(klines))
    return number[::-1].find('.')

def closing_price_list(klines):
    closing_price_list = []
    for count in range(len(klines)):
        closing_price_list.append(klines[count].get('close'))
    return closing_price_list

def previous_candle_color(klines):
    if previous_close(klines) > previous_open(klines): return "GREEN"
    elif previous_close(klines) < previous_open(klines): return "RED"
    else: return "INDECISIVE"

def candle_color(klines):
    if current_close(klines) > current_open(klines): return "GREEN"
    elif current_close(klines) < current_open(klines): return "RED"
    else: return "INDECISIVE"

def upper_wick(klines):
    if candle_color(klines) == "GREEN": return current_high(klines) - current_close(klines)
    elif candle_color(klines) == "RED": return current_high(klines) - current_open(klines)
    else: return 0

def lower_wick(klines):
    if candle_color(klines) == "GREEN": return current_open(klines)  - current_low(klines)
    elif candle_color(klines) == "RED": return current_close(klines) - current_low(klines)
    else: return 0

def strong_candle(klines):
    if candle_body(klines) > upper_wick(klines) or candle_body(klines) > lower_wick(klines):
        if candle_color(klines) == "GREEN":
            if previous_candle_color(klines) == "GREEN":
                if current_close(klines) > previous_close(klines): return True
            elif previous_candle_color(klines) == "RED":
                if current_close(klines) > previous_high(klines): return True
        
        elif candle_color(klines) == "RED":
            if previous_candle_color(klines) == "GREEN":
                if current_close(klines) < previous_low(klines): return True
            elif previous_candle_color(klines) == "RED":
                if current_close(klines) < previous_close(klines): return True
