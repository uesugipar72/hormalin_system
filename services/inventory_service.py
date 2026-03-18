import sqlite3
from config import DB_PATH

def update_inventory(
        chemical_id,
        action,
        quantity,
        counterparty_id,
        user_id):

    conn = sqlite3.connect(DB_PATH, timeout=30)
    cur = conn.cursor()

    try:

        # 現在在庫取得
        cur.execute(
            "SELECT quantity FROM inventory WHERE chemical_id=?",
            (chemical_id,)
        )

        row = cur.fetchone()

        # inventoryにデータが無い場合
        if row is None:

            before = 0

            cur.execute(
                "INSERT INTO inventory (chemical_id, quantity) VALUES (?,0)",
                (chemical_id,)
            )

        else:

            before = row[0]

        # 入出庫計算
        if action == "出庫":

            if before < quantity:
                raise ValueError("在庫不足")

            after = before - quantity

        else:

            after = before + quantity


        # 在庫更新
        cur.execute("""
        UPDATE inventory
        SET quantity=?
        WHERE chemical_id=?
        """,(after,chemical_id))


        # 履歴保存
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