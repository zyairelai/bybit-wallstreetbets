import os
import time
import config
from kucoin.client import Client

# Get environment variables
api_key        = os.environ.get('KUCOIN_KEY')
api_secret     = os.environ.get('KUCOIN_SECRET')
api_passphrase = os.environ.get('KUCOIN_PASSPHRASE')
spot_trading   = Client(api_key, api_secret, api_passphrase)
live_trade     = config.live_trade

def get_current_timestamp():
    return int(time.time() * 1000)

def get_timestamp(recent):
    return int(time.time()) - recent

pair, leverage = [], []
for i in range(len(config.coin)): pair.append(config.coin[i].upper() + "-USDT")

query = 20
def KLINE_INTERVAL_1HOUR(i): return spot_trading.get_kline_data(symbol=pair[i], kline_type="1hour", start=get_timestamp(query*60*60), end=get_current_timestamp())
def KLINE_INTERVAL_1DAY(i) : return spot_trading.get_kline_data(symbol=pair[i], kline_type="1day" , start=get_timestamp(query*24*60*60), end=get_current_timestamp())

klines = KLINE_INTERVAL_1HOUR(0)
