import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import openpyxl
from datetime import datetime

from utils.db_utils import get_connection


class InventoryFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        title = ttk.Label(
            self,
            text="在庫一覧",
            font=("Meiryo",16)
        )
        title.pack(pady=10)

        # -------------------------
        # 検索エリア
        # -------------------------

        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5)

        ttk.Label(search_frame,text="薬品名検索").grid(row=0,column=0,padx=5)

        self.search_entry = ttk.Entry(search_frame,width=30)
        self.search_entry.grid(row=0,column=1,padx=5)

        ttk.Button(
            search_frame,
            text="検索",
            command=self.search
        ).grid(row=0,column=2,padx=5)

        ttk.Button(
            search_frame,
            text="全表示",
            command=self.load_inventory
        ).grid(row=0,column=3,padx=5)

        # -------------------------
        # Treeview
        # -------------------------

        columns = ("name","qty","alert")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=20
        )

        self.tree.heading("name",text="薬品名")
        self.tree.heading("qty",text="在庫")
        self.tree.heading("alert",text="アラートレベル")

        self.tree.column("name",width=250)
        self.tree.column("qty",width=100)
        self.tree.column("alert",width=120)

        self.tree.pack(fill="both",expand=True,pady=10)

        # アラート色
        self.tree.tag_configure("alert",background="#ffcccc")

        # -------------------------
        # ボタン
        # -------------------------

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Excel出力",
            command=self.export_excel
        ).grid(row=0,column=0,padx=10)

        ttk.Button(
            btn_frame,
            text="更新",
            command=self.load_inventory
        ).grid(row=0,column=1,padx=10)

        ttk.Button(
            btn_frame,
            text="メニューに戻る",
            command=lambda: controller.show_frame("MenuFrame")
        ).grid(row=0,column=2,padx=10)

        self.load_inventory()

    # -------------------------
    # 在庫読込
    # -------------------------

    def load_inventory(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            c.name,
            i.quantity,
            i.alert_level
        FROM inventory i
        JOIN chemicals c
        ON i.chemical_id = c.id
        ORDER BY c.name
        """)

        rows = cur.fetchall()

        conn.close()

        self.tree.delete(*self.tree.get_children())

        for row in rows:

            name = row["name"]
            qty = row["quantity"]
            alert = row["alert_level"]

            tag = ""

            if qty <= alert:
                tag = "alert"

            self.tree.insert(
                "",
                "end",
                values=(name,qty,alert),
                tags=(tag,)
            )

    # -------------------------
    # 検索
    # -------------------------

    def search(self):

        keyword = self.search_entry.get()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            c.name,
            i.quantity,
            i.alert_level
        FROM inventory i
        JOIN chemicals c
        ON i.chemical_id = c.id
        WHERE c.name LIKE ?
        """,(f"%{keyword}%",))

        rows = cur.fetchall()

        conn.close()

        self.tree.delete(*self.tree.get_children())

        for row in rows:

            name = row["name"]
            qty = row["quantity"]
            alert = row["alert_level"]

            tag=""

            if qty <= alert:
                tag="alert"

            self.tree.insert(
                "",
                "end",
                values=(name,qty,alert),
                tags=(tag,)
            )

    # -------------------------
    # Excel出力
    # -------------------------

    def export_excel(self):

        try:

            wb = openpyxl.Workbook()
            ws = wb.active

            ws.title = "在庫一覧"

            ws.append(["薬品名","在庫","アラート"])

            for row_id in self.tree.get_children():

                row = self.tree.item(row_id)["values"]

                ws.append(row)

            filename = f"inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            wb.save(filename)

            messagebox.showinfo(
                "完了",
                f"Excel出力しました\n{filename}"
            )

        except Exception as e:

            messagebox.showerror(
                "エラー",
                str(e)
            )