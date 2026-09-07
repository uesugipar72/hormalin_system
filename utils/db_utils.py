import sqlite3
from config import DB_PATH

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def migrate_transaction_logs_action_check():
    """transaction_logs.action の CHECK制約に 'RETURN'（返却）を追加するマイグレーション。

    SQLiteはCHECK制約を直接変更できないため、制約が未更新（'RETURN'を含まない）
    の場合のみテーブルを作り直して移行する。既に移行済み、またはテーブル未作成
    の場合は何もしない（何度呼び出しても安全）。
    """

    conn = sqlite3.connect(DB_PATH)

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT sql FROM sqlite_master
            WHERE type = 'table' AND name = 'transaction_logs'
        """)
        row = cur.fetchone()

        if row is None or row[0] is None or "RETURN" in row[0]:
            return

        cur.execute("PRAGMA foreign_keys = OFF")

        cur.execute("""
            CREATE TABLE transaction_logs_new (
                "id"	INTEGER,
                "chemical_id"	INTEGER NOT NULL,
                "action"	TEXT NOT NULL CHECK("action" IN ('IN', 'OUT', 'RETURN')),
                "quantity"	REAL NOT NULL CHECK("quantity" > 0),
                "before_quantity"	REAL,
                "after_quantity"	REAL,
                "department_id"	INTEGER,
                "note"	TEXT,
                "created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
                "staff_id"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("chemical_id") REFERENCES "chemicals"("id")
            )
        """)

        cur.execute("""
            INSERT INTO transaction_logs_new (
                id, chemical_id, action, quantity, before_quantity,
                after_quantity, department_id, note, created_at, staff_id
            )
            SELECT
                id, chemical_id, action, quantity, before_quantity,
                after_quantity, department_id, note, created_at, staff_id
            FROM transaction_logs
        """)

        cur.execute("DROP TABLE transaction_logs")
        cur.execute("ALTER TABLE transaction_logs_new RENAME TO transaction_logs")

        cur.execute("""
            CREATE INDEX idx_logs_chemical
            ON transaction_logs (chemical_id)
        """)
        cur.execute("""
            CREATE INDEX idx_logs_created
            ON transaction_logs (created_at)
        """)

        cur.execute("PRAGMA foreign_keys = ON")

        conn.commit()

    finally:
        conn.close()
