from models.inventory_model import InventoryModel
from utils.db_utils import get_connection

class InventoryService:

    def __init__(self):

        self.model = InventoryModel()


    def stock_in(self, chemical_id, qty):

        before = self.model.get_quantity(chemical_id)

        after = before + qty

        self.model.update_quantity(chemical_id, after)


    def stock_out(self, chemical_id, qty):

        before = self.model.get_quantity(chemical_id)

        after = before - qty

        if after < 0:
            raise Exception("在庫不足")

        self.model.update_quantity(chemical_id, after)

    def get_inventory(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.name, i.quantity
            FROM inventory i
            JOIN chemicals c ON i.chemical_id = c.id
        """)

        rows = cursor.fetchall()
        conn.close()

        # dict形式に変換
        return [
            {"name": row[0], "qty": row[1]}
            for row in rows
        ]