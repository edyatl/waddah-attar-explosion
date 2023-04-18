#!/usr/bin/env python3
"""
    Python porting of Waddah Attar Explosion V2 [SHK] TradingView Indicator
    https://ru.tradingview.com/script/d9IjcYyS-Waddah-Attar-Explosion-V2-SHK/
    Developed by @edyatl <edyatl@yandex.ru> April 2023
    https://github.com/edyatl

"""
# Standard imports
import pandas as pd
import numpy as np
import talib as tl
import os
from os import environ as env
from dotenv import load_dotenv
from binance import Client

# Load API keys from env
project_dotenv = os.path.join(os.path.abspath(""), ".env")
if os.path.exists(project_dotenv):
    load_dotenv(project_dotenv)

api_key, api_secret = env.get("ENV_API_KEY"), env.get("ENV_SECRET_KEY")

# Make API Client instance
client = Client(api_key, api_secret)

short_col_names = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "qav",
    "num_trades",
    "taker_base_vol",
    "taker_quote_vol",
    "ignore",
]

# Load Dataset
# Get last 500 records of ATOMUSDT 15m Timeframe
klines = client.get_klines(symbol="ATOMUSDT", interval=Client.KLINE_INTERVAL_15MINUTE)
data = pd.DataFrame(klines, columns=short_col_names)

# Convert Open and Close time fields to DateTime
data["open_time"] = pd.to_datetime(data["open_time"], unit="ms")
data["close_time"] = pd.to_datetime(data["close_time"], unit="ms")

#--------------------------INPUTS--------------------------------
sensitivity: int = 150  # input(150, title='Sensitivity')
fastLength: int = 20  # input(20, title='FastEMA Length')
slowLength: int = 40  # input(40, title='SlowEMA Length')
channelLength: int = 20  # input(20, title='BB Channel Length')
mult: float = 2.0  # input(2.0, title='BB Stdev Multiplier')

# DEAD_ZONE = nz(ta.rma(ta.tr(true), 100)) * 3.7
# ta_tr = tl.TRANGE(data.high, data.low, data.close)
ta_rma = np.nan_to_num(tl.ATR(data.high, data.low, data.close, 100), nan=0)
DEAD_ZONE = ta_rma * 3.7

#--------------------------FUNCIONS------------------------------

def calc_macd(source, fastLength, slowLength):
    fastMA = tl.EMA(source, fastLength)
    slowMA = tl.EMA(source, slowLength)
    return fastMA - slowMA

def calc_BBUpper(source, length, mult):
    basis = tl.SMA(source, length)
    dev = mult * tl.STDDEV(source, length)
    return basis + dev

def calc_BBLower(source, length, mult):
    basis = tl.SMA(source, length)
    dev = mult * tl.STDDEV(source, length)
    return basis - dev

def main():
    close = data.close.to_numpy(dtype=np.double)
    close_1 = np.roll(close, 1)
    close_1[0] = 0

    t1 = (
        calc_macd(close, fastLength, slowLength)
        - calc_macd(close_1, fastLength, slowLength)
    ) * sensitivity

    e1 = calc_BBUpper(close, channelLength, mult) - calc_BBLower(close, channelLength, mult)

    trendUp = np.full_like(t1, fill_value=np.nan)
    trendDown = np.full_like(t1, fill_value=np.nan)

    for i in range(len(t1)):
        trendUp[i] = t1[i] if t1[i] >= 0 else 0
        trendDown[i] = t1[i] * -1 if t1[i] < 0 else 0

    res = pd.DataFrame(
        {
            "open_time": data["open_time"],
            "UpTrend": trendUp,
            "DownTrend": trendDown,
            "ExplosionLine": e1,
            "DeadZoneLine": DEAD_ZONE,
        }
    )
    res.to_csv('wae-ATOMUSDT-15m.csv', index = None, header=True)


if __name__ == "__main__":
    main()
