import sqlite3
from config import DB_PATH


def get_connection():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    return conn