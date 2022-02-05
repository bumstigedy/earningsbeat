from get_earnings import getEarnings
from get_prices import getPrices
import pandas as pd
from ta.momentum import RSIIndicator

if __name__ == "__main__":
    # df_earnings = getEarnings("AAPL")
    # df_prices = getPrices("AAPL")

    # print(df_earnings.head())
    # print(df_prices.head())
    # df_earnings.to_csv("earnings.csv", index=False)
    # df_prices.to_csv("prices.csv", index=False)
    df_earnings = pd.read_csv("earnings.csv")
    df_prices = pd.read_csv("prices.csv")
    # print(df_earnings.head())
    df_prices = df_prices.sort_values(by=["timestamp"])
    df_prices["shifted"] = df_prices.shift(periods=10).adjusted_close
    df_prices["pctChange"] = 100 * df_prices.shifted / df_prices.open
    # print(df_prices.head())
    # RSI_ind = RSIIndicator(df_prices.adjusted_close)
    # print(RSI_ind.rsi())
    df_prices["RSI"] = RSIIndicator(df_prices.adjusted_close).rsi()

    # RSI categories
    #  bullish overbought, oversold, neutral  bull market range is 40-90  50 or less oversold, 80 or more overbought
    # bearish overbought, oversold, neutral  bear market range is 10-60   50 or above is overbought 20 or lower is oversold
    df_prices["RSI_MAX"] = df_prices.RSI.rolling(30).max()
    df_prices["RSI_MIN"] = df_prices.RSI.rolling(30).min()
    # print(df_prices.tail(50))
    df_prices["status"] = ""
    # Bullish, Overboutht B_OB
    df_prices.loc[(df_prices.RSI_MAX >= 40) & (df_prices.RSI >= 80), "status"] = "B_OB"
    # Bullish, Oversold B_OS
    df_prices.loc[(df_prices.RSI_MAX >= 40) & (df_prices.RSI <= 50), "status"] = "B_OS"
    # Bullish, Neutral B_N
    df_prices.loc[
        (df_prices.RSI_MAX >= 40) & (df_prices.RSI > 50) & (df_prices.RSI < 80),
        "status",
    ] = "B_N"
    ##################
    # Bearish, Overboutht BR_OB
    df_prices.loc[(df_prices.RSI_MIN <= 40) & (df_prices.RSI >= 50), "status"] = "BR_OB"
    # Bearish, Oversold BR_OS
    df_prices.loc[(df_prices.RSI_MIN <= 40) & (df_prices.RSI <= 20), "status"] = "BR_OS"
    # Bearish, Neutral BR_N
    df_prices.loc[
        (df_prices.RSI_MIN <= 40) & (df_prices.RSI > 20) & (df_prices.RSI < 50),
        "status",
    ] = "BR_N"

    print(df_prices.tail())

# print out attributes of RSI Inidicator since documentation is not that good
# from pprint import pprint
# mylist = list()
# pprint(dir(RSIIndicator))
#########################Earnings##################################
df_earnings = df_earnings.sort_values(by="fiscalDateEnding")
df_earnings["surprise1"] = df_earnings.shift(periods=1).surprisePercentage
df_earnings["surprise2"] = df_earnings.shift(periods=2).surprisePercentage
df_earnings["surprise3"] = df_earnings.shift(periods=3).surprisePercentage
print(df_earnings.head())

df_merged = df_earnings.merge(
    df_prices, left_on="fiscalDateEnding", right_on="timestamp"
)
df_merged["target"] = df_merged.surprisePercentage.apply(lambda x: 1 if x > 0 else 0)
print(df_merged.head())
df_final = df_merged[
    ["SYMBOL_x", "target", "pctChange", "status", "surprise1", "surprise2", "surprise3"]
]
print("**20")
print(df_final.head())
