from models.inventory_model import InventoryModel


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