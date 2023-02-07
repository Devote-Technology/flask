import os
import psycopg2



db: str = os.environ.get("DB_NAME")
user: str = os.environ.get("DB_USER")
dbPassword: str = os.environ.get("DB_PASSWORD")
host: str = os.environ.get("DB_HOST")
port: str = os.environ.get("DB_PORT")

dbPassword = "1jL4urQKr2i4oHr8"


def getConnection():
  conn = psycopg2.connect(dbname="postgres", user="postgres", password=dbPassword,host="db.zkpmfmkldxumszdjxbse.supabase.co", port=5432)
  # conn = psycopg2.connect(dbname=db, user=user, password=dbPassword,host=host, port=port)
  return conn



