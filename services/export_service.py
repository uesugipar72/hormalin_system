import pandas as pd
import sqlite3
from config import DB_PATH

def export_logs():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""

    SELECT
    t.created_at as 日時,
    c.name as ホルマリン,
    t.action as 種別,
    t.quantity as 数量,
    cp.department_name as 相手先

    FROM transaction_logs t
    JOIN chemicals c
    ON t.chemical_id=c.id
    JOIN counterparties cp
    ON t.counterparty_id=cp.id

    """,conn)

    conn.close()

    df.to_excel("logs.xlsx",index=False)