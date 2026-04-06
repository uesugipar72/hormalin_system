import tkinter as tk
from tkinter import ttk


class HistoryFrame(ttk.Frame):

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