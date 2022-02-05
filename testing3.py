from get_earnings import getEarnings
from get_prices import getPrices
import pandas as pd
from ta.momentum import RSIIndicator

if __name__ == "__main__":
    df_earnings = getEarnings("QCOM")
    df_prices = getPrices("QCOM")

    print(df_earnings.head())
    print(df_prices.head())
