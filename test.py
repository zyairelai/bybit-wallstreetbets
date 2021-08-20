import os, candlestick, bybit, bybit_api, EMA

# Get environment variables
api_key    = os.environ.get('BYBIT_KEY')
api_secret = os.environ.get('BYBIT_SECRET')
client     = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

i = 0
quantity = 1
price = 0.3

klines = bybit_api.KLINE_INTERVAL_1DAY(i)
response = bybit_api.position_information(i)
dataset = candlestick.closing_price_list(klines)
decimal = candlestick.price_decimal_place(klines)

low  = EMA.compute(8, dataset, decimal)
mid  = EMA.compute(13, dataset, decimal)
high = EMA.compute(21, dataset, decimal)

print(bybit_api.limit_close_long(i, response))