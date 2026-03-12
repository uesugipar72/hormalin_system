import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from services.alert_service import check_inventory_alert
from services.master_service import (
    get_chemicals,
    get_counterparties,
    get_users
)

from services.inventory_service import update_inventory


DB_PATH = "database/hormalin.db"


class HormalinGUI(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("ホルマリン管理システム")
        self.geometry("700x500")

        self.chemical_dict = get_chemicals()
        self.counterparty_dict = get_counterparties()
        self.user_dict = get_users()

        self.create_widgets()

        self.load_inventory()

    # -------------------------
    # UI作成
    # -------------------------

    def create_widgets(self):

        frame = ttk.LabelFrame(self, text="入出庫入力")
        frame.pack(fill="x", padx=10, pady=10)

        # 種別
        ttk.Label(frame, text="ホルマリン種別").grid(row=0, column=0)

        self.chemical_combo = ttk.Combobox(
            frame,
            values=list(self.chemical_dict.keys()),
            width=20
        )
        self.chemical_combo.grid(row=0, column=1)

        # 入出庫
        ttk.Label(frame, text="種別").grid(row=0, column=2)

        self.action_combo = ttk.Combobox(
            frame,
            values=["入庫", "出庫"],
            width=10
        )
        self.action_combo.grid(row=0, column=3)

        # 個数
        ttk.Label(frame, text="個数").grid(row=0, column=4)

        self.qty_entry = ttk.Entry(frame, width=10)
        self.qty_entry.grid(row=0, column=5)

        # 相手先
        ttk.Label(frame, text="相手先").grid(row=1, column=0)

        self.counterparty_combo = ttk.Combobox(
            frame,
            values=list(self.counterparty_dict.keys()),
            width=20
        )
        self.counterparty_combo.grid(row=1, column=1)

        # 担当者
        ttk.Label(frame, text="担当者").grid(row=1, column=2)

        self.user_combo = ttk.Combobox(
            frame,
            values=list(self.user_dict.keys()),
            width=15
        )
        self.user_combo.grid(row=1, column=3)

        # 登録ボタン
        ttk.Button(
            frame,
            text="登録",
            command=self.register_data
        ).grid(row=1, column=5, pady=5)

        # -------------------
        # 在庫一覧
        # -------------------

        frame2 = ttk.LabelFrame(self, text="現在在庫")
        frame2.pack(fill="both", expand=True, padx=10, pady=10)

        self.inventory_tree = ttk.Treeview(
            frame2,
            columns=("name", "qty"),
            show="headings"
        )

        self.inventory_tree.heading("name", text="ホルマリン")
        self.inventory_tree.heading("qty", text="在庫")

        self.inventory_tree.pack(fill="both", expand=True)

        # -------------------
        # 履歴
        # -------------------

        frame3 = ttk.LabelFrame(self, text="取引履歴")
        frame3.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_tree = ttk.Treeview(
            frame3,
            columns=("date", "name", "action", "qty", "dept"),
            show="headings"
        )

        self.log_tree.heading("date", text="日時")
        self.log_tree.heading("name", text="ホルマリン")
        self.log_tree.heading("action", text="種別")
        self.log_tree.heading("qty", text="数量")
        self.log_tree.heading("dept", text="相手先")

        self.log_tree.pack(fill="both", expand=True)

        self.load_logs()

    # -------------------------
    # 登録処理
    # -------------------------

    def register_data(self):

        chemical_name = self.chemical_combo.get()
        action = self.action_combo.get()
        quantity = self.qty_entry.get()
        counterparty = self.counterparty_combo.get()

        if not chemical_name or not action or not quantity:

            messagebox.showerror("エラー", "入力してください")
            return

        quantity = int(quantity)

        chemical_id = self.chemical_dict[chemical_name]
        counterparty_id = self.counterparty_dict[counterparty]

        update_inventory(
            chemical_id,
            action,
            quantity,
            counterparty_id
        )

        messagebox.showinfo("完了", "登録しました")

        self.qty_entry.delete(0, tk.END)
        self.qty_entry.focus()

        self.load_inventory()
        self.load_logs()

    # -------------------------
    # 在庫表示
    # -------------------------

    def load_inventory(self):

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
        SELECT c.name,i.quantity
        FROM inventory i
        JOIN chemicals c
        ON i.chemical_id=c.id
        """)

        rows = cur.fetchall()

        self.inventory_tree.delete(*self.inventory_tree.get_children())

        for r in rows:
            self.inventory_tree.insert("", tk.END, values=r)

        conn.close()

    # -------------------------
    # 履歴表示
    # -------------------------

    def load_logs(self):

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
        SELECT
        t.created_at,
        c.name,
        t.action,
        t.quantity,
        cp.department_name
        FROM transaction_logs t
        JOIN chemicals c
        ON t.chemical_id=c.id
        JOIN counterparties cp
        ON t.counterparty_id=cp.id
        ORDER BY t.created_at DESC
        LIMIT 50
        """)

        rows = cur.fetchall()

        self.log_tree.delete(*self.log_tree.get_children())

        for r in rows:
            self.log_tree.insert("", tk.END, values=r)

        conn.close()