import math
import ccxt

exchange = "binance"
filename = 'feda_output.json'
interval = '1m'

pair = "ETHUSDT"
days = 30

class Feda:
    def __init__(self, fileName:str, pair:str, days:int, strExchange:str='binanceFutures'):
        self.fileName = fileName
        self.pair = pair
        self.days = days
        self.strExchange = strExchange
        self._checkExchange()

    def _checkExchange(self):
        if self.strExchange == 'binance':
            self.exchange = ccxt.binance({
                'enableRateLimit': True
            })

            self.limit = 1500
        elif self.strExchange == 'binanceFutures':
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

            self.limit = 1500

        elif self.strExchange == 'bybit':
            self.exchange = ccxt.bybit({
                'enableRateLimit': True
            })

            self.limit = 200
        elif self.strExchange == 'okexFutures':
            self.exchange = ccxt.okex({
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

            self.limit = 300
        elif self.strExchange == 'bitstamp':
            self.exchange = ccxt.bitstamp({
                'enableRateLimit': True
            })

            self.limit = 1000
        elif self.strExchange == 'ftx':
            self.exchange = ccxt.ftx({
                'enableRateLimit': True
            })

            self.limit = 5000
        else:
            raise Exception('Exchange is not supported')

    def fetchDatafeed(self):
        print('Fetching klines...')
        until = self.exchange.milliseconds()
        startSince = until - 86400000 * self.days

        diffBtwnUntilSince = round(int(until - startSince)/(1000*60))
        loopCount = math.floor(diffBtwnUntilSince / self.limit)

        fullOhlcv = self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe='1m', since=startSince)
        try:
            since = fullOhlcv[-1][0] + 60000
        except IndexError:
            raise Exception(f"{self.strExchange} doesn't provide data from this point on")

        fullOhlcvFull = fullOhlcv

        for i in range(loopCount):
            fullOhlcv = self.exchange.fetch_ohlcv(symbol=self.pair, limit=self.limit, timeframe='1m', since=since)
            fullOhlcvFull = fullOhlcvFull + fullOhlcv
            since = fullOhlcv[-1][0] + 60000
            print(since)

        f = open(self.fileName, "w")

        f.write(str(fullOhlcvFull))
        f.close()

        return fullOhlcv

datamanager = Feda(fileName=filename, pair=pair, days=days, strExchange=exchange)
ohlcv = datamanager.fetchDatafeed()