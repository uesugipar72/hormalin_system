import sqlite3
from utils.db_utils import get_connection
from constants.inventory_constants import (
    ACTION_MAP,
    ACTION_IN,
    ACTION_OUT,
    ACTION_DISPOSE
)


def update_inventory(
        chemical_id: int,
        action: str,
        quantity: int,
        counterparty_id: int,
        user_id: int):

    # -----------------------------
    # action を数値コードへ変換
    # -----------------------------
    action_code = ACTION_MAP.get(action)

    if action_code is None:
        raise ValueError(f"不正なaction: {action}")

    conn = get_connection()
    cur = conn.cursor()

    try:

        # -----------------------------
        # inventory レコード自動作成
        # -----------------------------
        cur.execute("""
        INSERT INTO inventory (chemical_id, quantity)
        SELECT ?, 0
        WHERE NOT EXISTS (
            SELECT 1 FROM inventory WHERE chemical_id = ?
        )
        """, (chemical_id, chemical_id))

        # -----------------------------
        # 現在在庫取得
        # -----------------------------
        cur.execute(
            "SELECT quantity FROM inventory WHERE chemical_id=?",
            (chemical_id,)
        )

        row = cur.fetchone()

        if row is None:
            raise ValueError("在庫レコード取得エラー")

        before = row["quantity"]

        # -----------------------------
        # 出庫
        # -----------------------------
        if action_code == ACTION_OUT:

            if before < quantity:
                raise ValueError("在庫不足")

            after = before - quantity

            cur.execute("""
            UPDATE inventory
            SET quantity = ?
            WHERE chemical_id = ?
            """, (after, chemical_id))

        # -----------------------------
        # 入庫
        # -----------------------------
        elif action_code == ACTION_IN:

            after = before + quantity

            cur.execute("""
            UPDATE inventory
            SET quantity = ?
            WHERE chemical_id = ?
            """, (after, chemical_id))

        # -----------------------------
        # 廃棄
        # -----------------------------
        elif action_code == ACTION_DISPOSE:

            if before < quantity:
                raise ValueError("廃棄数が在庫を超えています")

            after = before - quantity

            cur.execute("""
            UPDATE inventory
            SET quantity = ?
            WHERE chemical_id = ?
            """, (after, chemical_id))

        else:
            raise ValueError("未対応のaction")

        # -----------------------------
        # 履歴ログ保存
        # -----------------------------
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
            action_code,
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