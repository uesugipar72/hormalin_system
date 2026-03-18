from gui.login_gui import LoginGUI
from services.backup_service import backup_database
import logging


def main():

    try:
        # 起動時バックアップ
        backup_database()

    except Exception as e:
        logging.error(f"バックアップ失敗: {e}")

    # ログイン画面
    app = LoginGUI()
    app.mainloop()


if __name__ == "__main__":
    main()