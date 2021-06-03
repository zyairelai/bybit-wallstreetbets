import api_bybit

response = api_bybit.position_information(0)

# api_bybit.open_long_position(0)
# api_bybit.open_short_position(0)

# api_bybit.close_long(0)
# api_bybit.close_short(0)

# test = api_bybit.open_short_position(0)
# print(test)

for r in response:
    print(r)
# print(api_bybit.position_info(response))
