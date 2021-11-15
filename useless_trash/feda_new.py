import math
import ccxt
import pandas

class Feda:
    def __init__(self, fileName:str, pair:str, days:int, exchange:str='binanceFutures'):
        self.fileName = fileName
        self.pair = pair
        self.days = days
        self.exchange = exchange
        self._checkExchange()

    def _checkExchange(self):
        if self.exchange == 'binance':
            self.exchange = ccxt.binance({
                'enableRateLimit': True
            })

            self.limit = 1500
        elif self.exchange == 'binanceFutures':
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

            self.limit = 1500

        elif self.exchange == 'bybit':
            self.exchange = ccxt.bybit({
                'enableRateLimit': True
            })

            self.limit = 200
        elif self.exchange == 'okexFutures':
            self.exchange = ccxt.okex({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

            self.limit = 300
        elif self.exchange == 'bitstamp':
            self.exchange = ccxt.bitstamp({
                'enableRateLimit': True
            })

            self.limit = 1000
        elif self.exchange == 'ftx':
            self.exchange = ccxt.ftx({
                'enableRateLimit': True
            })

            self.limit = 5000
        else:
            raise Exception('Exchange is not supported')

    def fetchDatafeed(self, writeToFile=True):
        print('Fetching klines...')
        until = self.exchange.milliseconds()
        startSince = until - 86400000 * self.days

        diffBtwnUntilSince = round(int(until - startSince)/(1000*60))
        loopCount = math.floor(diffBtwnUntilSince / self.limit)

        fullOhlcv = self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe='1m', since=startSince)
        try:
            since = fullOhlcv[-1][0] + 60000
        except IndexError:
            raise Exception(f"{self.exchange} doesn't provide data from this point on")

        fullOhlcvFull = fullOhlcv

        for i in range(loopCount):
            fullOhlcv = self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe='1m', since=since)
            fullOhlcvFull = fullOhlcvFull + fullOhlcv
            since = fullOhlcv[-1][0] + 60000
            print(since)
        
        if writeToFile == True:
            f = open(self.fileName, "w")

            f.write(str(fullOhlcvFull))
            f.close()

        return fullOhlcvFull

datamanager = Feda( fileName='feda_output.json',
                    pair='BTCUSDT',
                    days=30,
                    exchange='binance')

data = datamanager.fetchDatafeed(writeToFile=False)
# data = datamanager.fetchDatafeed()

# Convert to desired interval range
interval = '5m'
# ohlcv = pandas.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
# ohlcv = ohlcv.set_index('date')
# ohlcv.index = pandas.to_datetime(ohlcv.index, unit='ms')
# ohlcv = ohlcv.groupby(pandas.Grouper(freq=interval)).agg({'open': 'first', 'high': max, 'low': min, 'close': 'last', 'volume': sum})
# print(ohlcv)