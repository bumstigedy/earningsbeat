import os
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import json
from conversions import convDate, convFloat

apiKey = os.getenv("ALPHA_VANTAGE")


def getPrices(symbol):
    """get a csv with prices for the input symbol"""
    symbol = symbol
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={key}&datatype=csv&outputsize=full".format(
        symbol=symbol, key=apiKey
    )
    df = pd.read_csv(url)
    df.timestamp = df.timestamp.apply(convDate)

    float_cols = [
        "open",
        "high",
        "low",
        "close",
        "adjusted_close",
        "volume",
        "dividend_amount",
        "split_coefficient",
    ]

    for col in float_cols:
        df[col] = df[col].apply(convFloat)

    df["SYMBOL"] = symbol
    return df
