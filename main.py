from gui.login_gui import LoginGUI
from services.backup_service import backup_database

if __name__ == "__main__":

    backup_database()

    app = LoginGUI()
    app.mainloop()