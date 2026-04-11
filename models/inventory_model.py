from utils.db_utils import get_connection


class InventoryModel:

    def get_quantity(self, chemical_id):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT quantity FROM inventory WHERE chemical_id=?",
            (chemical_id,)
        )

        row = cur.fetchone()

        conn.close()

        return row["quantity"] if row else 0


    def update_quantity(self, chemical_id, qty):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE inventory SET quantity=? WHERE chemical_id=?",
            (qty, chemical_id)
        )

        conn.commit()
        conn.close()