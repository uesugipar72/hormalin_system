from tkinter import ttk
from tkinter import messagebox


class LoginFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        ttk.Label(self,text="ログイン",font=("Meiryo",18)).pack(pady=30)

        ttk.Label(self,text="ユーザー").pack()

        self.user = ttk.Entry(self)
        self.user.pack()

        ttk.Label(self,text="パスワード").pack()

        self.password = ttk.Entry(self,show="*")
        self.password.pack()

        ttk.Button(
            self,
            text="ログイン",
            command=self.login
        ).pack(pady=20)

    def login(self):

        if self.user.get() == "admin":
            self.controller.show_frame("MenuFrame")
        else:
            messagebox.showerror("エラー","ログイン失敗")