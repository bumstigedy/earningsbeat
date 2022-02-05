import os
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import json
from conversions import convDate, convFloat

apiKey = os.getenv("ALPHA_VANTAGE")


symbol = "AAPL"
url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={key}&datatype=csv&outputsize=full".format(
    symbol=symbol, key=apiKey
)
df = pd.read_csv(url)
# df.timestamp = df.timestamp.apply(convDate)
print(url)
print(df.head())
