# seed_demo.py
import os
import sqlite3
from models import init_db, DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_PATH = os.path.join(BASE_DIR, "demo_data.sql")

init_db()
conn = sqlite3.connect(DB_PATH)
with open(SQL_PATH, encoding="utf-8") as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
print("Demo content loaded.")