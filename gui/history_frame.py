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
        columns = ("日時", "ホルマリン種", "区分", "数量", "担当者", "在庫", "備考")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.column("日時", width=160,anchor="center")
        self.tree.column("ホルマリン種", width=160,anchor="center")
        self.tree.column("区分", width=60,anchor="center")
        self.tree.column("数量", width=50,anchor="e")
        self.tree.column("担当者", width=120,anchor="center")
        self.tree.column("在庫", width=50,anchor="e")
        self.tree.column("備考", width=200,anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.sort_reverse = False  # 昇順/降順フラグ

        for col in columns:
            self.tree.heading(
                col,
                text=col,
                command=lambda c=col: self.sort_by_column(c)
            )

        # ▼ 戻るボタン
        ttk.Button(
            self,
            text="メニューに戻る",
            command=lambda: controller.show_frame("MenuFrame")
        ).pack(pady=10)

    def sort_by_column(self, col):

        col_index = self.tree["columns"].index(col)

        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            data.append((values[col_index], item))

        # ▼ ここを中に入れる！！
        def convert(value, col):
            if col == "日時":
                # YYYY年M月D日 → ソート用数値
                import re
                nums = list(map(int, re.findall(r"\d+", value)))
                return nums  # [2026, 5, 3]
            try:
                return float(value)
            except:
                return value

        data.sort(key=lambda x: convert(x[0], col), reverse=self.sort_reverse)

        for index, (_, item) in enumerate(data):
            self.tree.move(item, "", index)

        self.sort_reverse = not self.sort_reverse

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
            date_str = row[0][:10]
            y, m, d = date_str.split("-")
            row[0] = f"{int(y)}年{int(m)}月{int(d)}日"
            row[2] = action_map.get(row[2], row[2])# 数量の小数点を消す
            row[3] = int(row[3]) if row[3] is not None else 0
            row[5] = int(row[5]) if row[5] is not None else 0
            #row[7] = int(row[7]) if row[7] is not None else 0

            # ▼ フィルタ処理
            if selected != "すべて":
                if row[1] != selected:
                    continue

            self.tree.insert("", "end", values=row)

    def get_history_data(self):
        return get_history()