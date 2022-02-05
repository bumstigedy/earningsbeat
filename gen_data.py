from extract_data import extract_data
import pandas as pd
import time

if __name__ == "__main__":
    df_symbols = pd.read_csv("QQQ.csv")
    df_symbols = df_symbols.sort_values(by="SYMBOL")
    for symbol in df_symbols.SYMBOL:
        try:
            print(symbol)
            df = extract_data(symbol)
            print(df.head())
            time.sleep(60)  # pause in between calls so that the API doesn not fuss
        except:
            print("error for {}".format(symbol))
            time.sleep(300)  # wait longer and then try the symbol again
            try:
                print(symbol)
                df = extract_data(symbol)
                print(df.head())
                time.sleep(60)  # pause in between calls so that the API doesn not fuss
            except:
                print("giving up - error for {}".format(symbol))
                pass  # if it does not work the second time after waiting, give up
