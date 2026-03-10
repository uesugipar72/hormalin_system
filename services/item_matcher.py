import pandas as pd
from difflib import get_close_matches

# •i–ÚDB
items = pd.read_csv("data/items.csv")

def match_item(text):

    item_names = items["item_name"].tolist()

    match = get_close_matches(text, item_names, n=1, cutoff=0.5)

    if match:
        row = items[items["item_name"] == match[0]].iloc[0]
        return {
            "id": int(row["item_id"]),
            "name": row["item_name"]
        }

    return None