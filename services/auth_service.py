import sqlite3
from config import DB_PATH

def login(username,password):

    conn = sqlite3.connect(DB_PATH, timeout=30)
    cur = conn.cursor()

    cur.execute("""
    SELECT id,username,role
    FROM users
    WHERE username=? AND password=?
    """,(username,password))

    user = cur.fetchone()

    conn.close()

    return user