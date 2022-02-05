from extract_data import extract_data
import pandas as pd
import time

if __name__ == "__main__":
    df_symbols = pd.read_csv("QQQ.csv")
    df_symbols = df_symbols.sort_values(by="SYMBOL")
    for symbol in df_symbols.SYMBOL[0:3]:  ###### initially just do a few for testing
        try:
            print(symbol)
            df = extract_data(symbol)
            print(df.head())
            time.sleep(20)
        except:
            print("error for {}".format(symbol))
