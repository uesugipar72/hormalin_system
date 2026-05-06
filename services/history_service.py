import sqlite3
from config import DB_PATH

def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
       SELECT 
            t.created_at,
            c.name AS chemical_name,
            t.action,
            t.quantity,
            u.user_name AS user_name,
            t.note            
        FROM transaction_logs t
        LEFT JOIN chemicals c
        ON t.chemical_id = c.id
        LEFT JOIN users u
        ON t.staff_id = u.user_id
        ORDER BY t.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows