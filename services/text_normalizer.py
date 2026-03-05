import re

def normalize_text(text):
    replacements = {
        "出口": "出庫",
        "出荷": "出庫",
        "出汚": "出庫",
        "出稿": "出庫",
        "入荷": "入庫",
        "フォルマリン":"ホルマリン",
        "ナイシキョウ2":"内視鏡", 
        "ナンシュキョウ2":"内視鏡",
        "ナイシキョウ": "内視鏡",
        "内四強":"内視鏡",
        "内視強":"内視鏡",
        "ナイシキョウ":"内視鏡",
        "ホルマリン8ml":"8mlホルマリン",
        "ホルマリン8m":"8mlホルマリン",
        "8ミリリットルホルマリン": "8mlホルマリン",
        "シュッコ": "出庫",

     }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

def separate_action_and_number(text):

    text = re.sub(r'(出庫|入庫)(\d+)', r'\1 \2', text)

    return text
