from utils.db_utils import get_connection


def delete_last_transaction():

    conn = get_connection()
    cur = conn.cursor()

    try:

        # 最新transaction取得
        cur.execute("""
            SELECT
                id,
                formalin_type,
                action,
                quantity
            FROM transactions
            ORDER BY transaction_date DESC, id DESC
            LIMIT 1
        """)

        row = cur.fetchone()

        if not row:
            return False

        transaction_id = row[0]
        formalin_type = row[1]
        action = row[2]
        quantity = row[3]

        # 現在在庫取得
        cur.execute("""
            SELECT stock
            FROM stock
            WHERE formalin_type=?
        """, (formalin_type,))

        stock_row = cur.fetchone()

        current_stock = stock_row[0]

        # 在庫戻し
        if action == "IN":
            new_stock = current_stock - quantity

        elif action == "OUT":
            new_stock = current_stock + quantity

        else:
            raise Exception("不正なaction")

        # stock更新
        cur.execute("""
            UPDATE stock
            SET stock=?
            WHERE formalin_type=?
        """, (
            new_stock,
            formalin_type
        ))

        # transaction削除
        cur.execute("""
            DELETE FROM transactions
            WHERE id=?
        """, (transaction_id,))

        conn.commit()

        return True

    except:
        conn.rollback()
        raise

    finally:
        conn.close()