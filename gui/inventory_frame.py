from tkinter import ttk


class InventoryFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        self.user_label = ttk.Label(
            self,
            font=("Meiryo", 14)
        )
        self.user_label.pack(pady=20)

        ttk.Label(
            self,
            text="器材管理システム メイン画面"
        ).pack()

    def refresh(self):

        user = self.controller.current_user

        if user:
            self.user_label.config(
                text=f"{user['name']} さんログイン中"
            )