import shutil
import os
import datetime
from config import DB_PATH,BACKUP_DIR

def backup_database():

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    date = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    file = f"{BACKUP_DIR}/backup_{date}.db"

    shutil.copy(DB_PATH,file)