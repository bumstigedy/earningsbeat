import pandas as pd
import os

directory = "/media/sanjay/HDD2/tflow/earnings_est/spy/data/test"
tickers = []
beat_pcts = []

for filename in os.listdir(directory):

    df = pd.read_csv(
        "/media/sanjay/HDD2/tflow/earnings_est/spy/data/test/{}".format(filename)
    )
    beat_pct = 100 * len(df[df.target == 1]) / len(df)
    # print(filename, " :", beat_pct)
    tickers.append(filename.split(".")[0])
    beat_pcts.append(beat_pct)

df = pd.DataFrame(list(zip(tickers, beat_pcts)), columns=["ticker", "beat_pct"])
print(df.head())
print("----avg beat pct")
print(df.beat_pct.mean())
