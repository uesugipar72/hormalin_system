import tkinter as tk
from tkinter import ttk
from services.history_service import get_history

class HistoryFrame(ttk.Frame):
    window_size = "1000x700"
    resizable = (True, True)

    def __init__(self, parent, controller):

        super().__init__(parent)

        label = ttk.Label(
            self,
            text="取引履歴画面"
        )
        label.pack(pady=20)

        btn = ttk.Button(
            self,
            text="メニューに戻る",
            command=lambda: controller.show_frame("MenuFrame")
        )
        btn.pack()

    def refresh(self):
        # ① データ取得
        data = self.get_history_data()

        # ② 既存データ削除
        for row in self.tree.get_children():
            self.tree.delete(row)

        # ③ 再表示
        for row in data:
            self.tree.insert("", "end", values=row)

    def get_history_data(self):
        from services.history_service import get_history
        return get_history()