from gui.app import App
from utils.db_utils import migrate_transaction_logs_action_check

def main():

    migrate_transaction_logs_action_check()

    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
