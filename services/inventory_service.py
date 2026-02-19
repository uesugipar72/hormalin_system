import sqlite3

def update_inventory(name, qty, action):

    conn = sqlite3.connect("database/formalin.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM chemicals WHERE name=?", (name,))
    row = cursor.fetchone()

    if not row:
        print("薬品が登録されていません")
        return

    chemical_id = row[0]

    cursor.execute("SELECT quantity FROM inventory WHERE chemical_id=?", (chemical_id,))
    row = cursor.fetchone()

    current_qty = row[0] if row else 0

    if action == "IN":
        new_qty = current_qty + qty
    else:
        new_qty = current_qty - qty

    if new_qty < 0:
        print("在庫不足")
        return

    cursor.execute("""
        INSERT OR REPLACE INTO inventory (chemical_id, quantity)
        VALUES (?, ?)
    """, (chemical_id, new_qty))

    conn.commit()
    conn.close()
    print("登録完了")
