import bybit, os, api_bybit

api_key    = os.environ.get('api_bybit')
api_secret = os.environ.get('BYBIT_SECRET')
client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

# wjuuu = api_bybit.position_information(0)

print(client.LinearPositions.LinearPositions_myPosition(symbol="BTCUSDT", timestamp="1622784046").result())

