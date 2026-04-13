from tkinter import ttk
from tkinter import messagebox
from utils.db_utils import get_connection
from controllers.inventory_controller import InventoryController


class BaseTransactionFrame(ttk.Frame):

    action = None   # 入庫 / 出庫

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller
        self.inventory_controller = InventoryController()

        title = ttk.Label(
            self,
            text=f"{self.action}登録",
            font=("Meiryo", 16)
        )
        title.pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        # 薬品
        ttk.Label(form, text="薬品").grid(row=0, column=0, padx=10, pady=5)

        self.chemical_cb = ttk.Combobox(form, width=30)
        self.chemical_cb.grid(row=0, column=1)

        # 数量
        ttk.Label(form, text="数量").grid(row=1, column=0, padx=10, pady=5)

        self.qty_entry = ttk.Entry(form)
        self.qty_entry.grid(row=1, column=1)

        # 部署
        ttk.Label(form, text="部署").grid(row=2, column=0, padx=10, pady=5)

        if self.action == "入庫":
            self.counterparty_cb = ttk.Combobox(form, width=30, state="readonly")
        else:
            self.counterparty_cb = ttk.Combobox(form, width=30)

        self.counterparty_cb.grid(row=2, column=1)

        # 備考
        ttk.Label(form, text="備考").grid(row=3, column=0, padx=10, pady=5)

        self.note_entry = ttk.Entry(form, width=30)
        self.note_entry.grid(row=3, column=1)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="登録",
            command=self.register
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            btn_frame,
            text="メニューに戻る",
            command=lambda: controller.show_frame("MenuFrame")
        ).grid(row=0, column=1, padx=10)

        self.load_chemicals()
        self.load_counterparties()

    # -------------------
    # マスタ読込
    # -------------------

    def load_chemicals(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id,name FROM chemicals")

        rows = cur.fetchall()
        conn.close()

        self.chemical_dict = {
            row["name"]: row["id"]
            for row in rows
        }

        self.chemical_cb["values"] = list(self.chemical_dict.keys())

    def load_counterparties(self):

        conn = get_connection()
        cur = conn.cursor()

        if self.action == "入庫":
            # ★ デフォルト部署のみ取得
            cur.execute("""
                SELECT id, department_name
                FROM counterparties
                WHERE is_default = 1
            """)
        else:
            # ★ 全部署
            cur.execute("""
                SELECT id, department_name
                FROM counterparties
            """)

        rows = cur.fetchall()
        conn.close()

        self.counterparty_dict = {
            row["department_name"]: row["id"]
            for row in rows
        }

        self.counterparty_cb["values"] = list(self.counterparty_dict.keys())

        # 入庫時は自動選択
        if self.action == "入庫" and rows:
            default_name = rows[0]["department_name"]
            self.counterparty_cb.set(default_name)
            self.counterparty_cb["state"] = "disabled"
    # -------------------
    # 登録処理
    # -------------------

    def register(self):

        try:

            chemical_name = self.chemical_cb.get()
            qty = int(self.qty_entry.get())
            counterparty_name = self.counterparty_cb.get()
            if counterparty_name not in self.counterparty_dict:
                raise ValueError("取引先が選択されていません")
            note = self.note_entry.get()

            chemical_id = self.chemical_dict[chemical_name]
            counterparty_id = self.counterparty_dict[counterparty_name]

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO transaction_logs
                (chemical_id,action,quantity,counterparty_id,note)
                VALUES (?,?,?,?,?)
                """,
                (chemical_id, self.action, qty, counterparty_id, note)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("成功", f"{self.action}登録しました")

            self.clear_form()

        except Exception as e:

            messagebox.showerror("エラー", str(e))

    def clear_form(self):

        self.qty_entry.delete(0, "end")
        self.note_entry.delete(0, "end")