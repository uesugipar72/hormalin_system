import sqlite3
from config import DB_PATH

def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, name, qty
        FROM transaction_logs
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows