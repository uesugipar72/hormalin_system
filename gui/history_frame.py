import tkinter as tk
from tkinter import ttk
from services.history_service import get_history



class HistoryFrame(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="取引履歴画面").pack(pady=10)

        # ▼ Treeview追加（これがないと表示できない）
        columns = ("日時", "器材", "区分", "数量")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)

        ttk.Button(
            self,
            text="メニューに戻る",
            command=lambda: controller.show_frame("MenuFrame")
        ).pack(pady=10)

    def refresh(self):
        data = self.get_history_data()

        # 既存削除
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 再表示
        for row in data:
            self.tree.insert("", "end", values=row)

    def get_history_data(self):
        return get_history()