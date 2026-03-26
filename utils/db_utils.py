import sqlite3
from config import DB_PATH
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")

    return conn
