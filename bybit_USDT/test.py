import bybit_api
klines = bybit_api.get_klines(0)

def close(klines):
    closing_price_list = []
    for count in range(len(klines)):
        closing_price_list.append(klines[count].get('close'))
    return closing_price_list

def closing_price_list(klines):
    closing_price_list = []
    for entries in klines:
        closing_price_list.append(list(entries.values())[-2])
    return closing_price_list

print(close(klines))
print(closing_price_list(klines))