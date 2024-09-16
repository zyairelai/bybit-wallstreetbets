#!/bin/python3

import ccxt, time, os
from datetime import datetime
from pybit.unified_trading import HTTP 

exchange = ccxt.bybit()
client = HTTP(
    testnet=False,
    api_key=os.environ.get('BYBIT_KEY'),
    api_secret=os.environ.get('BYBIT_SECRET'))

def fetch_heikin_ashi(symbol='BTC/USDT', timeframe='1d'):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=3)
    ha_candles = []
    
    for i in range(len(ohlcv)):
        if i == 0:
            ha_open = (ohlcv[i][1] + ohlcv[i][4]) / 2
            ha_close = (ohlcv[i][1] + ohlcv[i][2] + ohlcv[i][3] + ohlcv[i][4]) / 4
        else:
            ha_open = (ha_candles[-1]['open'] + ha_candles[-1]['close']) / 2
            ha_close = (ohlcv[i][1] + ohlcv[i][2] + ohlcv[i][3] + ohlcv[i][4]) / 4
        
        ha_high = max(ohlcv[i][2], ha_open, ha_close)
        ha_low = min(ohlcv[i][3], ha_open, ha_close)
        
        ha_candles.append({
            'timestamp': ohlcv[i][0],
            'open': ha_open,
            'high': ha_high,
            'low': ha_low,
            'close': ha_close
        })
    
    return ha_candles[-1]  # Return the most recent Heikin-Ashi candle

def close_active_positions(symbol='BTCUSDT'):
    try:
        # Fetch open positions
        response = client.get_positions(category='linear', symbol=symbol)
        # print(response)
        position = response['result']['list'][0] if response['result']['list'] else None
        
        if position and position['size'] != '0':
            side = 'Sell' if position['side'] == 'Buy' else 'Buy'  # Determine the opposite side
            qty = position['size']
            
            # Place a market order to close the position
            close_response = client.place_order(
                symbol=symbol,
                side=side,
                order_type='Market',
                qty=0,  # Use actual quantity of the position
                reduce_only=True,  # Set reduce_only to true
                category='linear',  # Ensure correct category
                position_idx=0  # Use 0 for one-way mode
            )
            print(f"Closed position on {symbol} with side {side} and qty {qty}")
            # print(f"Close order response: {close_response}")
        else:
            print(f"No open position to close for {symbol}")
    
    except Exception as e:
        print(f"Error closing position: {e}")

def get_leverage(symbol):
    return int(client.get_positions(category="linear",symbol=symbol)['result']['list'][0]['leverage'])

def place_order(symbol='BTCUSDT', side='Buy', leverage=50, qty=0.01):
    current_leverage = get_leverage(symbol)
    
    if current_leverage and int(current_leverage) != leverage:
        client.set_leverage(
            symbol=symbol,
            category='linear',
            buyLeverage=str(leverage),
            sellLeverage=str(leverage)
        )
        print(f"Leverage set to {leverage} for {symbol}.")
    
    client.place_order(category="linear", symbol=symbol, side=side, qty=qty, order_type='Market')
    print(f"Placed {side} order on {symbol} with qty {qty}")

def wallstreetbet():
    symbol = 'BTCUSDT'
    leverage = 50
    trade_qty = 0.001

    ha_candle = fetch_heikin_ashi(symbol)
    body_size_pct = (abs(ha_candle['close'] - ha_candle['open']) / ha_candle['open']) * 100

    close_active_positions(symbol)
    time.sleep(60)

    if body_size_pct > 0.5:
        if ha_candle['close'] > ha_candle['open']:
            print(f"Going long on {symbol}")
            place_order(symbol, 'Buy', leverage, trade_qty)
        elif ha_candle['close'] < ha_candle['open']:
            print(f"Going short on {symbol}")
            place_order(symbol, 'Sell', leverage, trade_qty)
    else:
        print(f"Skipping trade on {symbol} due to small body size")

# Let's Get Rich
wallstreetbet()
