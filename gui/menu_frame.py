from tkinter import ttk


class MenuFrame(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        ttk.Label(self,text="メニュー",font=("Meiryo",18)).pack(pady=30)

        ttk.Button(
            self,
            text="入庫",
            command=lambda: controller.show_frame("StockInFrame")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="出庫",
            command=lambda: controller.show_frame("StockOutFrame")
        ).pack(pady=10)
        
        ttk.Button(
            self,
            text="在庫確認",
            command=lambda: controller.show_frame("InventoryFrame")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="取引履歴",
            command=lambda: controller.show_frame("HistoryFrame")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="劇毒物管理簿",
            command=lambda: controller.show_frame("PoisonLedgerFrame")
        ).pack(pady=10)    

        ttk.Button(
            self,
            text="マスタ設定",
            command=lambda: controller.show_frame("MasterFrame")
        ).pack(pady=10)

      # ★ 終了ボタン追加
        ttk.Button(
            self,
            text="終了",
            command=self.quit_app
        ).pack(pady=30)

    def quit_app(self):
        self.master.destroy()