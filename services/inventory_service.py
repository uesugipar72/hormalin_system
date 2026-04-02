import sqlite3
from config import DB_PATH
from utils.db_utils import get_connection
from constants.inventory_constants import ACTION_MAP


def update_inventory(
        chemical_id,
        action,
        quantity,
        counterparty_id,
        user_id):

    action_code = ACTION_MAP[action]

    conn = get_connection()
    cur = conn.cursor()


    try:

        # inventory レコードが無ければ作成
        cur.execute("""
        INSERT INTO inventory (chemical_id, quantity)
        SELECT ?, 0
        WHERE NOT EXISTS (
            SELECT 1 FROM inventory WHERE chemical_id = ?
        )
        """, (chemical_id, chemical_id))

        # 現在在庫取得
        cur.execute(
            "SELECT quantity FROM inventory WHERE chemical_id=?",
            (chemical_id,)
        )

        row = cur.fetchone()
        before = row["quantity"]

        # -------------------------
        # 出庫
        # -------------------------
        if action_code == ACTION_OUT:

            cur.execute("""
            UPDATE inventory
            SET quantity = quantity - ?
            WHERE chemical_id = ?
            AND quantity >= ?
            """, (quantity, chemical_id, quantity))

            if cur.rowcount == 0:
                raise ValueError("在庫不足")

            after = before - quantity

        # -------------------------
        # 入庫
        # -------------------------
        elif action == 1:

            cur.execute("""
            UPDATE inventory
            SET quantity = quantity + ?
            WHERE chemical_id = ?
            """, (quantity, chemical_id))

            after = before + quantity

        else:
            raise ValueError("不正なaction")

        # -------------------------
        # 履歴保存
        # -------------------------
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

    except Exception as e:

        conn.rollback()
        raise e

    finally:

        conn.close()