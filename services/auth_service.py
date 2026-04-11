import sqlite3
from config import DB_PATH

def login(user_id,password):

    conn = sqlite3.connect(DB_PATH, timeout=30)
    cur = conn.cursor()

    cur.execute("""
    SELECT id,user_id,user_name,role
    FROM users
    WHERE user_id=? AND password=?
    """, (user_id, password))

    row = cur.fetchone()

    conn.close()

    if row:
        return {
            "id": row[0],
            "user_id": row[1],
            "name": row[2],
            "role": row[3]
        }

    return None
