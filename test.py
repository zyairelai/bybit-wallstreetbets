import binance_futures_api
i = 0
response = binance_futures_api.position_information(i)

# see = abs(float(response.get('positionAmt')))

print(response)