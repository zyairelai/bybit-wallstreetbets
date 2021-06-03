import bybit_api

response = bybit_api.position_information(0)

# bybit_api.open_long_position(0)
# bybit_api.open_short_position(0)
# bybit_api.close_long(0, response)
# bybit_api.close_short(0, response)

test = bybit_api.open_long_position(0)

print(test)
