import sqlite3
from config import DB_PATH
import os

def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )
    db_path = DB_PATH
    print("DB接続先:", os.path.abspath(db_path))  # ★追加

    conn.execute("PRAGMA foreign_keys = ON")

    return conn