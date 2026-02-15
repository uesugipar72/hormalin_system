import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "formalin.db"

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    # ==========================
    # chemicals マスタ
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chemicals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        unit TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # inventory 現在在庫
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemical_id INTEGER NOT NULL,
        quantity REAL NOT NULL CHECK(quantity >= 0),
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chemical_id) REFERENCES chemicals(id) ON DELETE CASCADE
    );
    """)

    # ==========================
    # transaction_logs 入出庫履歴
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemical_id INTEGER NOT NULL,
        action TEXT CHECK(action IN ('IN','OUT')) NOT NULL,
        quantity REAL NOT NULL CHECK(quantity > 0),
        before_quantity REAL NOT NULL,
        after_quantity REAL NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chemical_id) REFERENCES chemicals(id)
    );
    """)

    # ==========================
    # users 操作ユーザー
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        role TEXT CHECK(role IN ('admin','operator')) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ==========================
    # インデックス
    # ==========================
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_inventory_chemical
    ON inventory (chemical_id);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_logs_chemical
    ON transaction_logs (chemical_id);
    """)

    conn.commit()


def insert_initial_data(conn):
    cursor = conn.cursor()

    # 初期薬品登録
    cursor.execute("""
    INSERT OR IGNORE INTO chemicals (name, unit)
    VALUES ('ホルマリン', 'L');
    """)

    # 初期ユーザー
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, role)
    VALUES ('admin', 'admin');
    """)

    conn.commit()


def create_triggers(conn):
    cursor = conn.cursor()

    # 在庫マイナス防止トリガー
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS prevent_negative_inventory
    BEFORE UPDATE ON inventory
    FOR EACH ROW
    WHEN NEW.quantity < 0
    BEGIN
        SELECT RAISE(ABORT, '在庫がマイナスになります');
    END;
    """)

    conn.commit()


def initialize_database():
    conn = create_connection()
    create_tables(conn)
    create_triggers(conn)
    insert_initial_data(conn)
    conn.close()
    print("✅ データベース初期化完了")


if __name__ == "__main__":
    initialize_database()
