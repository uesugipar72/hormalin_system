import sqlite3
from utils.db_utils import get_connection
def check_alert():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, i.quantity
        FROM inventory i
        JOIN chemicals c
        ON i.chemical_id = c.id
        WHERE i.quantity <= c.alert_level
    """)

    alerts = cur.fetchall()

    conn.close()

    return alerts