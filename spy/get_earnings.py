import os
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import json
from conversions import convDate, convFloat


def getEarnings(symbol):
    """get earnings from alpha vantage and return as df"""
    apiKey = os.getenv("ALPHA_VANTAGE")
    symbol = symbol

    url = "https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api}".format(
        symbol=symbol, api=apiKey
    )
    r = requests.get(url)
    data = r.json()
    df = pd.json_normalize(data, record_path="quarterlyEarnings")
    date_cols = ["fiscalDateEnding", "reportedDate"]

    for col in date_cols:
        df[col] = df[col].apply(convDate)

    float_cols = ["reportedEPS", "estimatedEPS", "surprise", "surprisePercentage"]

    for col in float_cols:
        df[col] = df[col].apply(convFloat)

    df["SYMBOL"] = symbol
    return df
