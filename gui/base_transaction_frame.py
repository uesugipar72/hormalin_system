from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.db_utils import get_connection
from controllers.inventory_controller import InventoryController
from gui.base_frame import BaseFrame



class BaseTransactionFrame(BaseFrame):

    action = None   # 入庫 / 出庫

    def __init__(self, parent, controller):

        super().__init__(parent,controller)

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
        label_text = "箱数" if self.action == "入庫" else "数量"
        ttk.Label(form, text=label_text).grid(row=1, column=0, padx=10, pady=5)

        self.qty_cb = ttk.Combobox(form, state="normal")
        self.qty_cb.grid(row=1, column=1)

        # 部署
        ttk.Label(form, text="部署").grid(row=2, column=0, padx=10, pady=5)

        if self.action == "入庫":
            self.department_cb = ttk.Combobox(form, width=30, state="readonly")
        else:
            self.department_cb = ttk.Combobox(form, width=30)

        self.department_cb.grid(row=2, column=1)

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

        # 初期ロード
        self.load_chemicals()
        self.load_department()   # ← 修正
        self.set_quantity_options()

    # -------------------
    # データロード
    # -------------------

    def load_chemicals(self):

        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, quantity_per_unit
            FROM chemicals
            ORDER BY display_order
            """)

        rows = cur.fetchall()
        conn.close()

        self.chemical_dict = {
            row["name"]: {
            "id": row["id"],
            "quantity_per_unit": row["quantity_per_unit"]
            }
            for row in rows
        }
        self.chemical_cb["values"] = list(self.chemical_dict.keys())

    def load_department(self):

        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if self.action == "入庫":
            cur.execute("""
                SELECT id, department_name
                FROM departments
                WHERE is_default = 1
            """)
        else:
            cur.execute("""
                SELECT id, department_name
                FROM departments
                ORDER BY display_order
            """)

        rows = cur.fetchall()
        conn.close()

        self.department_dict = {
            row["department_name"]: row["id"]
            for row in rows
        }

        self.department_cb["values"] = list(self.department_dict.keys())

        if self.action == "入庫" and self.department_dict:
            default_name = next(iter(self.department_dict))
            self.department_cb.set(default_name)
            self.department_cb["state"] = "disabled"

    # -------------------
    # 入力制御
    # -------------------

    def set_quantity_options(self):

        if self.action == "出庫":
            values = list(range(1, 41))
        else:
            values = list(range(1, 5))
        self.qty_cb["values"] = values

        vcmd = (self.qty_cb.register(self.validate_number), "%P")
        self.qty_cb.configure(validate="key", validatecommand=vcmd)

    def validate_number(self, P):
        return P.isdigit() or P == ""

    def get_action_code(self):
        return "IN" if self.action == "入庫" else "OUT"

    # -------------------
    # 登録処理
    # -------------------

    def register(self):

        try:
            chemical_name = self.chemical_cb.get()
            input_box_qty = int(self.qty_cb.get())
            chemical_data = self.chemical_dict[chemical_name]
            chemical_id = chemical_data["id"]
            quantity_per_unit = chemical_data["quantity_per_unit"]

            department_name = self.department_cb.get().strip()

            if department_name not in self.department_dict:
                raise ValueError("部署が選択されていません")

            note = self.note_entry.get()
            created_at = datetime.now(
                ZoneInfo("Asia/Tokyo")
            ).strftime("%Y-%m-%d %H:%M:%S")
            staff_id = self.controller.current_user_id
            department_id = self.department_dict[department_name]

            conn = get_connection()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # 在庫取得
            cur.execute("""
                SELECT quantity
                FROM inventory
                WHERE chemical_id = ?
            """, (chemical_id,))
            row = cur.fetchone()

            if row is None:
                before_qty = 0
                cur.execute("""
                    INSERT INTO inventory (chemical_id, quantity)
                    VALUES (?, 0)
                """, (chemical_id,))
            else:
                before_qty = row["quantity"]

            # 計算
            if self.action == "入庫":
                actual_qty = input_box_qty * quantity_per_unit
                after_qty = before_qty + actual_qty
                action_db = "IN"
            else:
                actual_qty = input_box_qty
                after_qty = before_qty - actual_qty
                if after_qty < 0:
                    raise ValueError("在庫不足です")
                action_db = "OUT"

            cur.execute("""
                UPDATE inventory
                SET quantity = ?
                WHERE chemical_id = ?
            """, (after_qty, chemical_id))

            # ログ登録
            cur.execute("""
                INSERT INTO transaction_logs
                (
                    chemical_id,
                    action,
                    quantity,
                    before_quantity,
                    after_quantity,
                    department_id,
                    staff_id,
                    note,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            """, (
                chemical_id,
                action_db,
                actual_qty,
                before_qty,
                after_qty,
                department_id,
                staff_id,
                note,
                created_at
            ))

            conn.commit()
            conn.close()
            before_qty = int(before_qty)
            after_qty = int(after_qty)

            messagebox.showinfo(
                f"{self.action}登録完了",
                f"薬品：{chemical_name}\n在庫：{before_qty} → {after_qty}"
            )

            self.reset_form()

        except Exception as e:
            messagebox.showerror("エラー", str(e))

    def reset_form(self):
        # コンボボックス
        self.chemical_cb.set("")
        self.qty_cb.set("")
        self.department_cb.set("")

        # Entry
        self.note_entry.delete(0, "end")

        # 入庫の場合はデフォルト再設定
        if self.action == "入庫" and self.department_dict:
            default_name = next(iter(self.department_dict))
            self.department_cb.set(default_name)

    def go_menu(self):
        self.controller.show_frame("MenuFrame")