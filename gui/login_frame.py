from tkinter import ttk
from tkinter import messagebox

from services.auth_service import login


class LoginFrame(ttk.Frame):

    window_size = "250x300"
    resizable = (False, False)

    def __init__(self, parent, controller):
        super().__init__(parent)

       

        self.controller = controller
        # 👇 ここに追加
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # コンテナ（中央寄せ用）
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # 中央ダイアログ
        main_frame = ttk.Frame(container, padding=20, relief="solid", borderwidth=1)
        main_frame.grid(row=0, column=0)

        ttk.Label(main_frame, text="ログイン", font=("Meiryo", 18)).grid(
            row=0, column=0, columnspan=2, pady=20
        )

        ttk.Label(main_frame, text="ユーザー").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.user_entry = ttk.Entry(main_frame, width=25)
        self.user_entry.grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="パスワード").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.pass_entry = ttk.Entry(main_frame, show="*", width=25)
        self.pass_entry.grid(row=2, column=1, pady=5)

        ttk.Button(main_frame, text="ログイン", command=self.login).grid(
            row=3, column=0, columnspan=2, pady=20
        )

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