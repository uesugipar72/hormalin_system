from ctypes.wintypes import SIZE
from tkinter import ttk


class InventoryFrame(ttk.Frame):

    window_size = "200x300"

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        self.user_label = ttk.Label(
            self,
            font=("Meiryo", 11)
        )
        self.user_label.pack(pady=20)

        ttk.Label(
            self,
            text="器材管理システム メイン画面"
        ).pack()

        style = ttk.Style()
        style.configure("Treeview", font=("Meiryo", 12), rowheight=28)
        style.configure("Treeview.Heading", font=("Meiryo", 10, "bold"))

        self.tree = ttk.Treeview(
            self,
            columns=("name", "qty"),
            show="headings"
        )

        self.tree.column("name", width=200)
        self.tree.column("qty", width=100, anchor="center")

        self.tree.heading("name", text="ホルマリン種別")
        self.tree.heading("qty", text="在庫数")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

       

    def load_inventory(self):

        # 既存データクリア
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 在庫データ取得（controller経由）
        inventory_list = self.controller.inventory_controller.get_inventory_list()
        
        # データ挿入
        for item in inventory_list:
            qty = int(float(item["qty"])) if item["qty"] else 0
            self.tree.insert(
                "",
                "end",
                values=(
                    item["name"],
                    qty
                )
            )

    def refresh(self):

        user = self.controller.current_user

        if user:
            self.user_label.config(
                text=f"{user['name']} さんログイン中"
            )
        self.load_inventory()