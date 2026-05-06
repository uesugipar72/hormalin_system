import tkinter as tk
from tkinter import ttk
from services.history_service import get_history


class HistoryFrame(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="取引履歴画面").pack(pady=10)

        # ▼ 抽出コンボボックス
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=5)

        ttk.Label(filter_frame, text="表示抽出").pack(side="left", padx=5)

        self.filter_cb = ttk.Combobox(
            filter_frame,
            values=[
                "すべて",
                "8mLホルマリン",
                "100mLホルマリン",
                "150mLホルマリン"
            ],
            state="readonly",
            width=20
        )
        self.filter_cb.set("すべて")
        self.filter_cb.pack(side="left", padx=5)

        # ▼ 抽出ボタン
        ttk.Button(
            filter_frame,
            text="抽出",
            command=self.refresh
        ).pack(side="left", padx=5)

        # ▼ Treeview
        columns = ("日時", "ホルマリン種", "区分", "数量", "担当者", "備考")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.column("日時", width=160)
        self.tree.column("ホルマリン種", width=160)
        self.tree.column("区分", width=60)
        self.tree.column("数量", width=50)
        self.tree.column("担当者", width=120)
        self.tree.column("備考", width=200)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)

        # ▼ 戻るボタン
        ttk.Button(
            self,
            text="メニューに戻る",
            command=lambda: controller.show_frame("MenuFrame")
        ).pack(pady=10)

    def refresh(self):
        data = self.get_history_data()

        action_map = {
            "IN": "入庫",
            "OUT": "出庫"
        }

        selected = self.filter_cb.get()

        # ▼ 既存削除
        for row in self.tree.get_children():
            self.tree.delete(row)

        # ▼ 再表示（フィルタ付き）
        for row in data:
            row = list(row)

            # 区分変換
            row[2] = action_map.get(row[2], row[2])
            # ▼ フィルタ処理
            if selected != "すべて":
                if row[1] != selected:
                    continue

            self.tree.insert("", "end", values=row)

    def get_history_data(self):
        return get_history()