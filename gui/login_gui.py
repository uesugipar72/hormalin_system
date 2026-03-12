import tkinter as tk
from tkinter import ttk,messagebox
from services.auth_service import login

class LoginGUI(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("ログイン")
        self.geometry("300x200")

        ttk.Label(self,text="ユーザー").pack()

        self.user_entry = ttk.Entry(self)
        self.user_entry.pack()

        ttk.Label(self,text="パスワード").pack()

        self.pass_entry = ttk.Entry(self,show="*")
        self.pass_entry.pack()

        ttk.Button(
            self,
            text="ログイン",
            command=self.login
        ).pack(pady=20)

    def login(self):

        user = login(
            self.user_entry.get(),
            self.pass_entry.get()
        )

        if user:

            self.destroy()

            from gui.inventory_gui import InventoryGUI

            app = InventoryGUI(user)
            app.mainloop()

        else:

            messagebox.showerror("エラー","ログイン失敗")