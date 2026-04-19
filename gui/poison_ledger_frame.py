from tkinter import ttk
from utils.db_utils import get_connection
from constants.inventory_constants import ACTION_CODE_LABEL
import sqlite3
class PoisonLedgerFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="劇毒物管理簿", font=("Meiryo", 16)).pack(pady=10)

        # -----------------------------
        # タブ作成
        # -----------------------------
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.tabs = {}
        self.treeviews = {}

        self.load_poison_chemicals()

    # -----------------------------
    # 劇毒物（ホルマリンサイズ別）取得
    # -----------------------------
    def load_poison_chemicals(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name
            FROM chemicals
            WHERE is_poison = 1
        """)

        rows = cur.fetchall()
        conn.close()

        self.chemicals = rows

        for row in rows:
            chem_id = row["id"]
            chem_name = row["name"]

            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=chem_name)

            self.tabs[chem_id] = tab

            self.create_tree(tab, chem_id)

    # -----------------------------
    # Treeview作成
    # -----------------------------
    def create_tree(self, parent, chemical_id):

        columns = (
            "date",
            "action",
            "quantity",
            "balance",
            "department",
            "staff",
            "usage"
        )

        tree = ttk.Treeview(parent, columns=columns, show="headings")

        tree.heading("date", text="日付")
        tree.heading("action", text="区分")
        tree.heading("quantity", text="数量")
        tree.heading("balance", text="残量")
        tree.heading("department", text="部署")
        tree.heading("staff", text="取扱者")
        tree.heading("usage", text="用途")

        for col in columns:
            tree.column(col, anchor="center", width=100)

        tree.pack(fill="both", expand=True)

        self.treeviews[chemical_id] = tree

        self.load_logs(chemical_id)

    # -----------------------------
    # ログ読み込み
    # -----------------------------
    def load_logs(self, chemical_id):

        conn = get_connection()
        conn.row_factory = sqlite3.Row  # ← これ重要（dict形式で取得）
        cur = conn.cursor()

        cur.execute("""
        SELECT
            p.created_at,
            p.action,
            p.quantity,
            p.after_quantity,
            p.note,
            c.name AS chemical_name,
            u.user_name AS name,
            d.department_name AS department_name
        FROM poison_logs p
        JOIN chemicals c ON p.chemical_id = c.id
        JOIN users u ON p.user_id = u.id
        LEFT JOIN departments d ON p.department_id = d.id
        WHERE p.chemical_id = ?
        """, (chemical_id,))

        rows = cur.fetchall()
        conn.close()

        tree = self.treeviews[chemical_id]

        # クリア
        for item in tree.get_children():
            tree.delete(item)

        # データ挿入
        for row in rows:
            action = ACTION_CODE_LABEL.get(row["action"], row["action"])

            tree.insert("", "end", values=(
                row["created_at"],
                action,
                row["quantity"],
                row["after_quantity"],
                row["department_name"],
                row["name"],
                row["note"]
            ))