from tkinter import ttk


class MasterFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        ttk.Label(
            self,
            text="マスタ設定",
            font=("Meiryo",16)
        ).pack(pady=20)

        ttk.Button(
            self,
            text="薬品マスタ",
            command=self.open_chemical
        ).pack(pady=10)

        ttk.Button(
            self,
            text="取引先マスタ",
            command=self.open_counterparty
        ).pack(pady=10)

        ttk.Button(
            self,
            text="ユーザーマスタ",
            command=self.open_user
        ).pack(pady=10)

        ttk.Button(
            self,
            text="メニューに戻る",
            command=lambda: controller.show_frame("MenuFrame")
        ).pack(pady=20)


    def open_chemical(self):

        print("薬品マスタ画面")

    def open_counterparty(self):

        print("取引先マスタ画面")

    def open_user(self):

        print("ユーザーマスタ画面")