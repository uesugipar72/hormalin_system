import shutil
import os
import datetime
from config import DB_PATH,BACKUP_DIR
from utils.db_utils import get_connection


def backup_database():

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    date = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    file = f"{BACKUP_DIR}/backup_{date}.db"

    shutil.copy(DB_PATH,file)

def create_daily_snapshot():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO inventory_daily_snapshot
    (snapshot_date, chemical_id, quantity)
    SELECT
    DATE('now'),
    chemical_id,
    quantity
    FROM inventory
    """)

    conn.commit()
    conn.close()