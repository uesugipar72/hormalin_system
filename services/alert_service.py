import sqlite3
from config import DB_PATH,ALERT_LEVEL
from utils.db_utils import get_connection
def check_alert():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT c.name,i.quantity
    FROM inventory i
    JOIN chemicals c
    ON i.chemical_id=c.id
    """)

    rows = cur.fetchall()

    conn.close()

    alerts = []

    for name,qty in rows:

        if qty <= ALERT_LEVEL:
            alerts.append((name,qty))

    return alerts