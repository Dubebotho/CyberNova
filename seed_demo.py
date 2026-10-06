# seed_demo.py
import sqlite3
from models import init_db

init_db()
conn = sqlite3.connect("database.db")
conn.executescript(open("demo_data.sql", encoding="utf-8").read())
conn.commit()
conn.close()
print("Demo content loaded.")