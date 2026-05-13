from tkinter import ttk


class BaseFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        # ヘッダー
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=5)

        # ログインユーザー名
        self.user_label = ttk.Label(
            header,
            font=("Meiryo", 10),
        )

        self.user_label.pack(side="right")


    def refresh_user_display(self):

        user_name = self.controller.current_user_name


        self.user_label.config(
             text=f"👤: {user_name}"
        )