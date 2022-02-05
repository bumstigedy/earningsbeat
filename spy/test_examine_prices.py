import pandas as pd
import plotly.express as px

df = pd.read_csv("/media/sanjay/HDD2/tflow/earnings_est/spy/data/timestamp/A.csv")
print(df.head())
print(df.columns)

fig = px.line(df, x="reportedDate", y="surprise")
fig.show()
