import sqlite3

def update_inventory(item_id, action, qty):

    conn = sqlite3.connect("formalin.db")

    cur = conn.cursor()

    if action == "入庫":

        cur.execute("""
        UPDATE items
        SET stock = stock + ?
        WHERE item_id = ?
        """,(qty,item_id))

    else:

        cur.execute("""
        UPDATE items
        SET stock = stock - ?
        WHERE item_id = ?
        """,(qty,item_id))

    conn.commit()
    conn.close()
