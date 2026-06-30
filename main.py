#main.py
from db_connection import DatabaseConnection
from logger_setup import setup_logger
import logging
import account_system
from menu import Menu

def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Program started")
    
    while True:
        active_account = account_system.main()
        if active_account:
            logger.info(f"User {active_account.user_id} logged in")
            menu = Menu()
            menu.main_menu()
        else:
            logger.info("No active account, exiting")
            break

if __name__ == "__main__":
    main()