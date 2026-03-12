import sqlite3
from config import DB_PATH

def update_inventory(
        chemical_id,
        action,
        quantity,
        counterparty_id,
        user_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT quantity FROM inventory WHERE chemical_id=?",
        (chemical_id,)
    )

    before = cur.fetchone()[0]

    if action == "出庫":
        after = before - quantity
    else:
        after = before + quantity

    cur.execute("""
    UPDATE inventory
    SET quantity=?
    WHERE chemical_id=?
    """,(after,chemical_id))

    cur.execute("""
    INSERT INTO transaction_logs
    (
        chemical_id,
        action,
        quantity,
        before_quantity,
        after_quantity,
        counterparty_id,
        user_id
    )
    VALUES (?,?,?,?,?,?,?)
    """,
    (
        chemical_id,
        action,
        quantity,
        before,
        after,
        counterparty_id,
        user_id
    ))

    conn.commit()
    conn.close()