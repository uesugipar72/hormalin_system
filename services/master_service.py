import sqlite3
from config import DB_PATH
from utils.db_utils import get_connection

def get_chemicals():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id,name FROM chemicals")

    rows = cur.fetchall()

    conn.close()

    return {name:id for id,name in rows}


def get_counterparties():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT id,department_name
    FROM counterparties
    """)

    rows = cur.fetchall()

    conn.close()

    return {name:id for id,name in rows}