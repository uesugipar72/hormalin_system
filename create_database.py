import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "hormalin.db"
print (f"📂 データベースパス: {DB_PATH}")

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_indexes(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_inventory_chemical
    ON inventory(chemical_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_logs_chemical
    ON transaction_logs(chemical_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_logs_created
    ON transaction_logs(created_at)
    """)

    conn.commit()


def create_tables(conn):
    cursor = conn.cursor()

    # ==========================
    # chemicals
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
    # users
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        role TEXT CHECK(role IN ('admin','operator')) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 🔥 これが不足している
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS counterparties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE
    );
    """)

    # ==========================
    # transaction_types
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_types (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    """)

    # ==========================
    # transactions
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemical_id INTEGER NOT NULL,
        transaction_type_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        counterparty_id INTEGER,
        user_id INTEGER,
        note TEXT,
        transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chemical_id) REFERENCES chemicals(id),
        FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(id),
        FOREIGN KEY (counterparty_id) REFERENCES counterparties(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # ==========================
    # inventory
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemical_id INTEGER NOT NULL,
        quantity REAL NOT NULL CHECK(quantity >= 0),
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chemical_id) REFERENCES chemicals(id)
    );
    """)

    # ==========================
    # snapshot
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_daily_snapshot(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_date DATE NOT NULL,
        chemical_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(snapshot_date, chemical_id),
        FOREIGN KEY (chemical_id) REFERENCES chemicals(id)
    );
    """)
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS poison_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemical_id INTEGER,
        user_id INTEGER,
        department_id INTEGER,
        action TEXT,
        quantity INTEGER,
        after_quantity INTEGER,
        note TEXT,
        created_at TEXT,
        FOREIGN KEY (chemical_id) REFERENCES chemicals(id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
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
    try:
        conn = create_connection()  # ← 修正

        create_tables(conn)
        create_indexes(conn)
        create_triggers(conn)

        conn.commit()
        conn.close()

        print("✅ データベース初期化完了")

    except Exception as e:
        print("❌ エラー:", e)


if __name__ == "__main__":
    initialize_database()
