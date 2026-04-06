import tkinter as tk
from tkinter import ttk
from controllers.inventory_controller import InventoryController


class StockOutFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.inventory_controller = InventoryController()

        self.chemical_id = ttk.Entry(self)
        self.chemical_id.pack()

        self.qty = ttk.Entry(self)
        self.qty.pack()

        ttk.Button(
            self,
            text="出庫",
            command=self.register
        ).pack()


    def register(self):

        chemical_id = int(self.chemical_id.get())
        qty = int(self.qty.get())

        self.inventory_controller.stock_out(
            chemical_id,
            qty
        )