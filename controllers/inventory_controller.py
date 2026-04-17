from services.inventory_service import InventoryService


class InventoryController:

    def __init__(self):

        self.service = InventoryService()
        

    def stock_in(self, chemical_id, qty):

        self.service.stock_in(chemical_id, qty)


    def stock_out(self, chemical_id, qty):

        self.service.stock_out(chemical_id, qty)