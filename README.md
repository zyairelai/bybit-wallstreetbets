## TABLE OF CONTENTS

1. [LONG-TERM-LOW-LEVERAGE](#long_term_low_leverage)
2. [DISCLAIMER](#hello_disclaimer)
3. [HOW-IT-WORKS](#how_it_works)
4. [HOW-TO-USE](#how_to_use)
    1. [ENVIRONMENT SETUP](#environment_setup)
    2. [PIP3 REQUIREMENTS](#pip3_requirements)
    3. [CONFIGURATIONS](#configurations)
    4. [RUN](#run)
5. [JOIN-MY-DISCORD](#discord)
    - [QUICK ACCESS TO THE DARK DIMENSION](https://discord.gg/r4TnhcdqmT)

<a name="long_term_low_leverage"></a>
## LONG-TERM-LOW-LEVERAGE
This is a trading bot that suupports **Binance USDT-M Futures** and **Bybit USDT Perpetual**

Inspired by [THE 5-8-13 STRATEGY](https://www.dolphintrader.com/5-8-13-forex-scalping-trading-strategy/). But Simpler and more practical after some tweaks.  

You can check my daily PnL [HERE ON MY GOOGLE SHEET](https://docs.google.com/spreadsheets/d/1VsOY7B7WWT0D67ifggpbsdHrQEegl0DaXHfWhsx--tY/edit#gid=210739304)  

<a name="hello_disclaimer"></a>
## DISCLAIMER
I have no responsibility for any loss or hardship incurred directly or indirectly by using this code.

PLEASE MANAGE YOUR RISK LEVEL BEFORE USING MY SCRIPT.

USE IT AT YOUR OWN RISK!

<a name="how_it_works"></a>
## HOW-IT-WORKS

1. As usual, with the 5-8-13 EMA, however we do not look at whether it is UPTREND nor DOWNTREND.  

2. We only focus on the candle size, to consider a good strong candle, its candle body shall be bigger than the sum of the both wicks.  

3. For LONG position, it triggers a buy order if it is a **GREEN STRONG CANDLE** that the close hits above the **MIDDLE** line.  

4. It will close the LONG position if the close hits below the **TOP** line.  

5. For SHORT position, it triggers a sell order if it is a **RED STRONG CANDLE** that the close hits below the **MIDDLE** line.  

6. It will close the SHORT position if the close hits above the **BOTTOM** line.  

7. The default and the most recommended interval is `1D` timeframe.  

8. You can calculate your desired trade amount by running `python3 cal_tradeAmt.py`

<a name="how_to_use"></a>
## HOW-TO-USE
<a name="environment_setup"></a>
### 1. ENVIRONMENT SETUP
Setup your environment API key on the Terminal:
```
export BINANCE_KEY="your_binance_api_key"
export BINANCE_SECRET="your_binance_secret_key"

export BYBIT_KEY="your_bybit_api_key"
export BYBIT_SECRET="your_bybit_secret_key"
```

Or as an alternative, you can change `line 6-9` in `binance_futures_api.py` or `bybit_api.py` to following:  
For `binance_futures_api.py`
```
api_key     = "your_binance_api_key"
api_secret  = "your_binance_secret_key"
```
For `bybit_api.py`
```
api_key     = "your_bybit_api_key"
api_secret  = "your_bybit_secret_key"
```

<a name="pip3_requirements"></a>
### 2. PIP3 REQUIREMENTS
You need to have these libraries installed:
```
pip3 install APScheduler==3.6.3
pip3 install Bybit==0.2.12
pip3 install cryptography==3.3.2
pip3 install pandas==1.2.4
pip3 install python-binance==0.7.5
pip3 install termcolor==1.1.0
```

<a name="configurations"></a>
### 3. CONFIGURATIONS
Before running, maybe you want to see how the output looks like.  
The settings can be configured in `config.py`.

| Variables           | Description                                                                                                |
| --------------------| -----------------------------------------------------------------------------------------------------------|
| `live_trade`        |`True` to place actual order <br /> `False` to see sample output                                            |
| `enable_scheduler`  |`True` to loop the code everytime when the minute hits 0 and 30, which means twice in one hour              |
| `coin`              | You can put your coin list here                                                                            |
| `quantity`          | Amount of the trade amount you want to trade                                                               |
| `leverage`          | The recommended leverage is all listed in the `config.py`. For BTC it is 30x, other coins shall below 20x  |

<a name="run"></a>
### 4. RUN
If you want to time this script by your own, set `enable_scheduler = False` then you can make your own scheduler

Else, you can set `enable_scheduler = True` and the script will loop the program for you every 30 minutes.

Now if you are all ready, set `live_trade = True` and ...

Let's make the magic happens!

### Command to on Binance
```
python3 trade_binance.py
```

### Command to on Binance
```
python3 trade_bybit.py
```

<a name="discord"></a>
## [JOIN MY DISCORD - QUICK ACCESS TO THE DARK DIMENSION](https://discord.gg/r4TnhcdqmT)
