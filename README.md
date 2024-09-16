# Wall-Street-Bet
1. Close any active trades at UTC 00:00, regardless of profit or loss.
2. Wait 1 minute after closing the trade.
3. Check the 1D Heikin-Ashi candle at UTC 00:00.
4. If the 1D Heikin-Ashi candle is green and its body size is bigger than 0.5%, go long.
5. If the candle is red and its body size is bigger than 0.5%, go short.
6. If the body is smaller than 0.5%, skip the trade.

This strategy is simple and revolves around daily Heikin-Ashi candles, focusing on body size for direction and skipping indecisive candles.

### PIP3 REQUIREMENTS
```
pip3 install -r requirements.txt
```
Or if you prefer to install these libraries one by one:
```
pip3 install ccxt
pip3 install pandas
pip3 install pybit
pip3 install python-binance
```
