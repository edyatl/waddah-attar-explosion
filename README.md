## Python porting of Waddah Attar Explosion V2 [SHK] TradingView Indicator


>Developed by [@edyatl](https://github.com/edyatl) April 2023 <edyatl@yandex.ru>

### Using [Python wrapper](https://github.com/TA-Lib/ta-lib-python) for [TA-LIB](http://ta-lib.org/) based on Cython instead of SWIG.

### Original Indicator code

```python
//
// @author LazyBear 
// List of all my indicators: 
// https://docs.google.com/document/d/15AGCufJZ8CIUvwFJ9W-IKns88gkWOKBCvByMEvm5MLo/edit?usp=sharing
//

// Modified for Crypto Market by ShayanKM

study("Waddah Attar Explosion V2 [SHK]", shorttitle="WAE [SHK]")
sensitivity = input(150, title="Sensitivity")
fastLength=input(20, title="FastEMA Length")
slowLength=input(40, title="SlowEMA Length")
channelLength=input(20, title="BB Channel Length")
mult=input(2.0, title="BB Stdev Multiplier")

DEAD_ZONE = nz(rma(tr(true),100)) * 3.7

calc_macd(source, fastLength, slowLength) =>
    fastMA = ema(source, fastLength)
    slowMA = ema(source, slowLength)
    fastMA - slowMA

calc_BBUpper(source, length, mult) => 
    basis = sma(source, length)
    dev = mult * stdev(source, length)
    basis + dev

calc_BBLower(source, length, mult) => 
    basis = sma(source, length)
    dev = mult * stdev(source, length)
    basis - dev

t1 = (calc_macd(close, fastLength, slowLength) - calc_macd(close[1], fastLength, slowLength))*sensitivity

e1 = (calc_BBUpper(close, channelLength, mult) - calc_BBLower(close, channelLength, mult))

trendUp = (t1 >= 0) ? t1 : 0
trendDown = (t1 < 0) ? (-1*t1) : 0

plot(trendUp, style=columns, linewidth=1, color=(trendUp<trendUp[1])?lime:green, transp=45, title="UpTrend")
plot(trendDown, style=columns, linewidth=1, color=(trendDown<trendDown[1])?orange:red, transp=45, title="DownTrend")
plot(e1, style=line, linewidth=2, color=#A0522D, title="ExplosionLine")
plot(DEAD_ZONE, color=blue, linewidth=1, style=cross, title="DeadZoneLine")
```

### Original Indicator Overview

**The Waddah Attar Explosion V2 [SHK]** is a popular trading indicator ported from MT4 to TradingView by LazyBear in response to user requests and  modified for crypto market by ShayanKM. The indicator tracks trend direction and strength using MACD/BB and **is best suited for use on a 30-minute time frame**. The indicator has various components, including the **Dead Zone Line**, which acts as a filter for weak signals. Trades should not be taken when the red or green histogram is below this line.

The red histogram represents the current downtrend, while the green histogram represents the current uptrend. The sienna line shows the explosion in price up or down. To enter a buy trade, several conditions must be met. The green histogram must be rising and above **the Explosion line**, which must also be rising. Both the green histogram and Explosion line should be above the **Dead Zone Line**.

To exit a buy trade, traders should exit when the green histogram crosses below **the Explosion line**. To enter a sell trade, the red histogram must be rising and above **the Explosion line**, which must also be rising. Both the red histogram and Explosion line should be above **the Dead Zone Line**. To exit a sell trade, traders should exit when the red histogram crosses below the Explosion line.

All the parameters of the indicator are configurable via the options page, and traders may need to tune the settings to their specific instrument. One modification of the indicator was made to adapt it to low-price markets like cryptocurrency, where **the Dead Zone Line** is based on **ATR** instead of a fixed number. Overall, **the Waddah Attar Explosion V2 [SHK]** is a useful indicator for tracking trend direction and strength and can be used in a range of markets with the right tuning of settings.


