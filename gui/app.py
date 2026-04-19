import tkinter as tk
from tkinter import ttk

from gui.login_frame import LoginFrame
from gui.menu_frame import MenuFrame
from gui.stock_in_frame import StockInFrame
from gui.stock_out_frame import StockOutFrame
from gui.history_frame import HistoryFrame
from gui.inventory_frame import InventoryFrame
from gui.master_frame import MasterFrame
from gui.poison_ledger_frame import PoisonLedgerFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.current_user = None
        self.title("ホルマリン管理システム")
        self.geometry("400x300")  # ← サイズも調整

        # 👇 gridに統一
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        # 👇 これも重要（中央配置効かせる）
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame_classes = (
            LoginFrame,
            MenuFrame,
            StockInFrame,
            StockOutFrame,
            HistoryFrame,
            InventoryFrame,
            PoisonLedgerFrame,
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