import sqlite3
from config import DB_PATH

def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.created_at,
            d.department_name,
            c.name,              -- 試薬名(ホルマリン種)
            t.action,
            t.quantity,
            t.user_name,
            t.stock_after,
            t.remark
        FROM transaction_logs t

        LEFT JOIN departments d
            ON t.department = d.department_id

        LEFT JOIN chemicals c
            ON t.chemical_id = c.chemical_id

        ORDER BY t.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows