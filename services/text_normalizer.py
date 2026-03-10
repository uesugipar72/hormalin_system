import re

def normalize_text(text):
    REPLACE_DICT = {
        "出口": "出庫",
        "出荷": "出庫",
        "出汚": "出庫",
        "出稿": "出庫",
        "入荷": "入庫",
        "オルマリン": "ホルマリン",
        "ホルマリン液": "ホルマリン",
        "8ミリ": "8ml",
        "10ミリ": "10ml",
        "20ミリ": "20ml",
        "内し今日": "内視鏡"
     }

    def normalize_text(text):

        for k, v in REPLACE_DICT.items():
            text = text.replace(k, v)

        return text
