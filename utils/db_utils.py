import sqlite3
import sys
from pathlib import Path

# プロジェクトルートを追加
sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import DB_PATH


def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")

    return conn