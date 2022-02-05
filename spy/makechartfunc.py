import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import glob
import os

#
def makeChart(symbol):
    df = pd.read_csv(
        "/media/sanjay/HDD2/tflow/earnings_est/spy/results/{}".format(symbol)
    )
    for col in df.columns.to_list():
        print(col)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    fig.add_trace(
        go.Candlestick(
            x=df["timestamp_x"],
            open=df["open_x"],
            high=df["high_x"],
            low=df["low_x"],
            close=df["close_x"],
            name="price",
        ),
        row=1,
        col=1,
    )

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.add_trace(
        go.Scatter(
            x=df.timestamp_x, y=df.RSI_x, mode="lines", name="RSI", line_color="black"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.timestamp_x, y=df.pred_probab, mode="markers", name="beat probability"
        ),
        row=3,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df.timestamp_x,
            y=df.target,
            mode="markers",
            marker_color="red",
            marker_symbol="x-open-dot",
            name="beat:1 / miss: 0",
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"},
        title="{} Prediction vs Actual".format(ticker.split(".")[0]),
        font=dict(family="Courier New, monospace", size=18, color="black"),
    )

    # fig.show()

    fig.write_html(
        "/media/sanjay/HDD2/tflow/earnings_est/spy/charts/{}.html".format(
            symbol.split(".")[0]
        )
    )
    return ""


if __name__ == "__main__":
    # makeChart("GOOGL")
    os.chdir("/media/sanjay/HDD2/tflow/earnings_est/spy/results")
    tickerList = glob.glob("*.csv")
    for ticker in tickerList:
        makeChart(ticker)
