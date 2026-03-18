import tkinter as tk
from tkinter import ttk,messagebox
from services.inventory_service import update_inventory
from services.master_service import (
    get_chemicals,
    get_counterparties
)

from services.inventory_service import update_inventory
from services.alert_service import check_alert


class InventoryGUI(tk.Tk):

    def __init__(self,user):

        super().__init__()

        self.user_id = user[0]
        self.username = user[1]
        self.role = user[2]

        self.title(f"ホルマリン管理 {self.username}")

        self.geometry("500x400")

        self.chemical_dict = get_chemicals()
        self.counterparty_dict = get_counterparties()

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(self,text="ホルマリン").pack()

        self.chemical_combo = ttk.Combobox(
            self,
            values=list(self.chemical_dict.keys())
        )
        self.chemical_combo.pack()

        ttk.Label(self,text="入出庫").pack()

        self.action_combo = ttk.Combobox(
            self,
            values=["入庫","出庫"]
        )
        self.action_combo.pack()

        ttk.Label(self,text="数量").pack()

        self.qty_entry = ttk.Entry(self)
        self.qty_entry.pack()

        ttk.Label(self,text="相手先").pack()

        self.counterparty_combo = ttk.Combobox(
            self,
            values=list(self.counterparty_dict.keys())
        )
        self.counterparty_combo.pack()

        ttk.Button(
            self,
            text="登録",
            command=self.register
        ).pack(pady=20)

    def register(self):

        chemical = self.chemical_combo.get()
        action = self.action_combo.get()

        try:
            qty = int(self.qty_entry.get())
        except:
            messagebox.showerror("エラー","数字入力")
            return

        counterparty = self.counterparty_combo.get()

        chemical_id = self.chemical_dict[chemical]
        counterparty_id = self.counterparty_dict[counterparty]

        update_inventory(
            chemical_id,
            action,
            qty,
            counterparty_id,
            self.user_id
        )

        alerts = check_alert()

        if alerts:

            msg = ""

            for name,qty in alerts:
                msg += f"{name} 在庫{qty}\n"

            messagebox.showwarning("在庫警告",msg)

        messagebox.showinfo("完了","登録しました")

        self.qty_entry.delete(0,tk.END)
        self.qty_entry.focus()