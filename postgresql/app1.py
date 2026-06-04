import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

print(Path.cwd())
load_dotenv(Path.cwd()/".env")
url=os.getenv("DATABASE_URL")
print(url)
connection_status_sql=False
try:
    connection_postgresql=psycopg2.connect(url) 
    connection_status_sql=True
except Exception as e:
    connection_postgresql=False

print(connection_status_sql)