from get_earnings import getEarnings
from get_prices import getPrices
import pandas as pd
from ta.momentum import RSIIndicator


def extract_data(symbol):
    df_earnings = getEarnings(symbol)
    df_prices = getPrices(symbol)
    df_prices = df_prices.sort_values(by=["timestamp"])
    df_prices["shifted"] = df_prices.shift(periods=10).close
    df_prices["pctChange"] = 100 * df_prices.shifted / df_prices.open
    df_prices["RSI"] = RSIIndicator(df_prices.close).rsi()
    df_prices["RSI_MAX"] = df_prices.RSI.rolling(30).max()
    df_prices["RSI_MIN"] = df_prices.RSI.rolling(30).min()
    df_prices["status"] = ""
    ######## Bullish Cases ###########################################################
    # Bullish, Overboutht B_OB
    df_prices.loc[(df_prices.RSI_MAX >= 40) & (df_prices.RSI >= 80), "status"] = "B_OB"
    # Bullish, Oversold B_OS
    df_prices.loc[(df_prices.RSI_MAX >= 40) & (df_prices.RSI <= 50), "status"] = "B_OS"
    # Bullish, Neutral B_N
    df_prices.loc[
        (df_prices.RSI_MAX >= 40) & (df_prices.RSI > 50) & (df_prices.RSI < 80),
        "status",
    ] = "B_N"
    ######## Bearish Cases ###########################################################
    # Bearish, Overboutht BR_OB
    df_prices.loc[(df_prices.RSI_MIN <= 40) & (df_prices.RSI >= 50), "status"] = "BR_OB"
    # Bearish, Oversold BR_OS
    df_prices.loc[(df_prices.RSI_MIN <= 40) & (df_prices.RSI <= 20), "status"] = "BR_OS"
    # Bearish, Neutral BR_N
    df_prices.loc[
        (df_prices.RSI_MIN <= 40) & (df_prices.RSI > 20) & (df_prices.RSI < 50),
        "status",
    ] = "BR_N"

    #########################Earnings##################################
    df_earnings = df_earnings.sort_values(by="fiscalDateEnding")
    df_earnings["surprise1"] = df_earnings.shift(periods=1).surprisePercentage
    df_earnings["surprise2"] = df_earnings.shift(periods=2).surprisePercentage
    df_earnings["surprise3"] = df_earnings.shift(periods=3).surprisePercentage

    df_merged = df_earnings.merge(
        df_prices, left_on="reportedDate", right_on="timestamp"
    )
    df_merged["target"] = df_merged.surprisePercentage.apply(
        lambda x: 1 if x > 0 else 0
    )

    # save a version with alll the data including the timestamp so we can analyze the results vs trends
    df_merged.to_csv(
        "/media/sanjay/HDD2/tflow/earnings_est/spy/data/timestamp/{}.csv".format(
            symbol
        ),
        index=False,
    )

    df_final = df_merged[
        [
            "SYMBOL_x",
            "target",
            "pctChange",
            "status",
            "surprise1",
            "surprise2",
            "surprise3",
        ]
    ]
    df_final = df_final.rename(columns={"SYMBOL_x": "SYMBOL"})
    df_final.to_csv(
        "/media/sanjay/HDD2/tflow/earnings_est/spy/data/{}.csv".format(symbol),
        index=False,
    )
    return df_final
