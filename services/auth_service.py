import sqlite3
from config import DB_PATH

def login(user_id,password):

    conn = sqlite3.connect(DB_PATH, timeout=30)
    cur = conn.cursor()

    cur.execute("""
    SELECT id,user_id,role
    FROM users
    WHERE user_id=? AND password=?
    """, (user_id, password))

    user = cur.fetchone()

    conn.close()

    return user
