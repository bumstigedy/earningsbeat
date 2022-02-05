import psycopg2
from sqlalchemy import create_engine
import os

#
postgres_user = os.getenv("POSTGRES_USER")
postgres_pw = os.getenv("POSTGRES_PW")

conn = psycopg2.connect(
    host="localhost", database="earnings", user=postgres_user, password=postgres_pw
)

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/earnings")

# df_tweets.to_sql('tweets',con=engine,index=False)
