import sqlite3

DB_PATH = "formalin.db"

def load_items():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM chemicals")

    items = [row[0] for row in cur.fetchall()]

    conn.close()

    return items


def detect_item(text):

    items = load_items()

    for item in items:
        if item in text:
            return item

    return None