from tkinter import ttk
from tkinter import messagebox
from utils.db_utils import get_connection
from controllers.inventory_controller import InventoryController


class BaseTransactionFrame(ttk.Frame):

    action = None   # 入庫 / 出庫

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller
       
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

        self.qty_cb = ttk.Combobox(form, state="normal")  # ←入力も可能
        self.qty_cb.grid(row=1, column=1)


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

        # ボタン
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
        self.set_quantity_options()
        

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

        # dict作成
        self.counterparty_dict = {
            row["department_name"]: row["id"]
            for row in rows
        }

        # コンボボックスにセット
        self.counterparty_cb["values"] = list(self.counterparty_dict.keys())

        # ★ 入庫時はデフォルト固定
        if self.action == "入庫" and self.counterparty_dict:
            default_name = next(iter(self.counterparty_dict))
            self.counterparty_cb.set(default_name)
            self.counterparty_cb["state"] = "disabled"

    def load_staff(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name
            FROM users
        """)

        rows = cur.fetchall()
        conn.close()

        self.staff_dict = {
            row["name"]: row["id"]
            for row in rows
        }

    def set_quantity_options(self):

        if self.action == "出庫":
            values = list(range(1, 41))
        else:
            values = [20, 24, 50, 100, 150, 200, 250, 300]

        self.qty_cb["values"] = values

        vcmd = (self.qty_cb.register(self.validate_number), "%P")
        self.qty_cb.configure(validate="key", validatecommand=vcmd)


    def validate_number(self, P):
        return P.isdigit() or P == ""

    def get_action_code(self):
        if self.action == "入庫":
            return "IN"
        elif self.action == "出庫":
            return "OUT"
        else:
            raise ValueError("不正な操作です")

    # -------------------
    # 登録処理
    # -------------------

    def register(self):
        action_db = self.get_action_code()

        try:
            chemical_name = self.chemical_cb.get()
            qty = float(self.qty_cb.get())
            counterparty_name = self.counterparty_cb.get().strip()
            if counterparty_name not in self.counterparty_dict:
                raise ValueError("取引先が選択されていません")

            note = self.note_entry.get()
            staff_id = self.controller.current_user_id
            chemical_id = self.chemical_dict[chemical_name]
            counterparty_id = self.counterparty_dict[counterparty_name]

            conn = get_connection()
            cur = conn.cursor()

            # ① 現在在庫取得
            cur.execute("""
                SELECT quantity
                FROM inventory
                WHERE chemical_id = ?
            """, (chemical_id,))
            row = cur.fetchone()

            if row is None:
                raise ValueError("在庫データが存在しません")

            before_qty = row["quantity"]

            # ② after計算
            if self.action == "入庫":
                after_qty = before_qty + qty
            elif self.action == "出庫":
                after_qty = before_qty - qty
                if after_qty < 0:
                    raise ValueError("在庫不足です")
            else:
                raise ValueError("不正な操作です")

            # ③ 在庫更新
            cur.execute("""
                UPDATE inventory
                SET quantity = ?
                WHERE chemical_id = ?
            """, (after_qty, chemical_id))

            # ④ ログ登録
            cur.execute("""
                INSERT INTO transaction_logs
                (chemical_id, action, quantity, before_quantity, after_quantity, counterparty_id, staff_id, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chemical_id,
                action_db,
                qty,
                before_qty,
                after_qty,
                counterparty_id,
                staff_id,
                note
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                f"{self.action}登録完了",
                f"薬品：{chemical_name}\n在庫：{before_qty} → {after_qty}"
            )
            self.clear_form()

        except Exception as e:
            messagebox.showerror("エラー", str(e))

    def clear_form(self):
        self.controller.show_frame("MenuFrame")