import os
import time
import bybit

# Get environment variables
api_key    = os.environ.get('BYBIT_API')
api_secret = os.environ.get('BYBIT_SECRET')
client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

print(client.Common.Common_getTime().result()[0])

