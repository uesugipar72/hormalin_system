import sqlite3
from config import DB_PATH
from utils.db_utils import get_connection
def monthly_usage():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

    SELECT
    c.name,
    SUM(t.quantity)

    FROM transaction_logs t
    JOIN chemicals c
    ON t.chemical_id=c.id

    WHERE t.action='出庫'

    GROUP BY c.name

    """)

    rows = cur.fetchall()

    conn.close()

    return rows