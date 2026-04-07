from tkinter import ttk


class InventoryFrame(ttk.Frame):

    def __init__(self, parent, user):

        super().__init__(parent)

        ttk.Label(
            self,
            text=f"{user['name']} さんログイン中",
            font=("Meiryo", 14)
        ).pack(pady=20)

        ttk.Label(
            self,
            text="器材管理システム メイン画面"
        ).pack()