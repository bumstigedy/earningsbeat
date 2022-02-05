import pandas as pd


def convDate(string):
    """convert to date time"""
    return pd.to_datetime(string)


def convFloat(string):
    """convert to float"""
    if string == "None":  # replace blanks with 0
        return 0
    return float(string)
