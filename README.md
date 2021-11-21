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
This is a trading bot for **Binance USDT-M Futures**. 

Inspired by [SHORT TERM STRATEGIES THAT WORK](https://www.amazon.com/Short-Term-Trading-Strategies-That/dp/0981923909) by Larry Connors.  

<a name="hello_disclaimer"></a>
## DISCLAIMER
I have no responsibility for any loss or hardship incurred directly or indirectly by using this code.

PLEASE MANAGE YOUR RISK LEVEL BEFORE USING MY SCRIPT.

USE IT AT YOUR OWN RISK!

<a name="how_it_works"></a>
## HOW-IT-WORKS

1. This strategy theory is "Buy Pullbacks, not breakouts!"

2. This strategy check on the daily timeframe.

3. The bot will initiate a buy position if the current daily close is lower than the previous 7 days low.

4. A buy position also means placing a LONG order and closing the SHORT position together.

5. The bot will initiate a sell position if the current daily close is higher than the previous 7 days high.

6. A sell position also means placing a SHORT order and closing the LONG position, together.

7. There will be a trailing stop with a call back rate of 5%, if you set `use_trailing = True` 

8. The backtest result is using `OPEN` of the candle instead of `CLOSE`, therefore the backtest result will be similar to real trades.

<a name="how_to_use"></a>
## HOW-TO-USE
<a name="environment_setup"></a>
### 1. ENVIRONMENT SETUP
Setup your environment API key on the Terminal:
```
export BINANCE_KEY="your_binance_api_key"
export BINANCE_SECRET="your_binance_secret_key"
```

Or as an alternative, you can change `line 6-9` in `binance_futures_api.py` to following:  
```
api_key     = "your_binance_api_key"
api_secret  = "your_binance_secret_key"
```
Don't forget the `" "` symbol to make your API key into `STRING` type!  

**I WILL NO LONGER ANSWER QUESTION REGARDING TO THIS ERROR:**
```
AttributeError: 'NoneType' object has no attribute 'encode'
``` 
**QUICK GOOGLE SEARCH or FIX YOUR API KEY**  
**DO NOT SPAM MY EMAIL AND DISTURB MY PEACEFUL LIFE LOL**

<a name="pip3_requirements"></a>
### 2. PIP3 REQUIREMENTS
You need to have these libraries installed:
```
pip3 install ccxt
pip3 install pandas
pip3 install termcolor
pip3 install python-binance
pip3 install cryptography==3.4.6
```

<a name="configurations"></a>
### 3. CONFIGURATIONS
Before running, maybe you want to see how the output looks like.  
The settings can be configured in `config.py`.

| Variables           | Description                                                                                                |
| --------------------| -----------------------------------------------------------------------------------------------------------|
| `live_trade`        |`True` to place actual order <br /> `False` to see sample output                                            |
| `use_trailing`      |`True` to set a Trailing Stop <br /> `False` to not using Trailing Stop                                     |
| `callbackrate`      | Check https://www.binance.com/en/support/faq/360042299292                                                  |
| `coin`              | You can put your coin list here                                                                            |
| `quantity`          | Amount of the trade amount you want to trade                                                               |
| `leverage`          | The recommended leverage is all listed in the `config.py`.                                                 |

<a name="run"></a>
### 4. RUN

Now if you are all ready, set `live_trade = True` and ...

Let's make the magic happens!

### Command to on Binance
```
python3 trade_binance.py
```

**Note:** The command above will only execute the code once.  
Therefore you need to create your own cronjob or scheduler to keep the code running!  
Since the code will check on the daily close, it is recommended to set your timer at 00:00 UTC everyday.

<a name="discord"></a>
## [JOIN MY DISCORD - QUICK ACCESS TO THE DARK DIMENSION](https://discord.gg/r4TnhcdqmT)
