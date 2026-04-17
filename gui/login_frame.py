from tkinter import ttk
from tkinter import messagebox

from services.auth_service import login


class LoginFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        ttk.Label(self, text="ログイン", font=("Meiryo", 18)).pack(pady=30)

        ttk.Label(self, text="ユーザー").pack()

        self.user_entry = ttk.Entry(self)
        self.user_entry.pack()

        ttk.Label(self, text="パスワード").pack()

        self.pass_entry = ttk.Entry(self, show="*")
        self.pass_entry.pack()

        ttk.Button(
            self,
            text="ログイン",
            command=self.login
        ).pack(pady=20)

        # Enterキー
        self.user_entry.bind("<Return>", self.focus_password)
        self.pass_entry.bind("<Return>", self.enter_login)

        self.user_entry.focus()

    def focus_password(self, event):

        self.pass_entry.focus()

    def enter_login(self, event):

        self.login()

    def login(self):

        user = login(
            self.user_entry.get(),
            self.pass_entry.get()
        )

        if user:
            # ログインユーザー保存
            self.controller.current_user = user
            # メイン画面へ
            self.controller.current_user_id = user["id"]
            self.controller.show_frame("MenuFrame")
            
        else:

            messagebox.showerror("エラー", "ログイン失敗")