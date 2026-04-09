import tkinter as tk
from tkinter import ttk

from gui.login_frame import LoginFrame
from gui.menu_frame import MenuFrame
from gui.stock_in_frame import StockInFrame
from gui.stock_out_frame import StockOutFrame
from gui.history_frame import HistoryFrame
from gui.inventory_frame import InventoryFrame
from gui.master_frame import MasterFrame


class App(tk.Tk):

    def __init__(self):

        super().__init__()

        self.current_user = None
        self.title("ホルマリン管理システム")
        self.geometry("300x600")

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        frame_classes = (
            LoginFrame,
            MenuFrame,
            StockInFrame,
            StockOutFrame,
            HistoryFrame,
            InventoryFrame,
            MasterFrame
        )

        for F in frame_classes:

            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, name):

        frame = self.frames[name]

        if hasattr(frame, "refresh"):
            frame.refresh()

        frame.tkraise()