#main.py
from db_connection import DatabaseConnection
from logger_setup import setup_logger
import logging
import account_system
from menu import Menu
from vehicle_ui import VehicleUI
from user_interface import PartUI,CarUI,MaintenanceUI
from part_manager import PartManager
from part_repository import PartRepository
from db_connection import DatabaseConnection
from car_manager import CarManager
from maintenance_manager import MaintenanceManager
from car_repository import CarRepository
from service import MaintenanceService

def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Program started")

    db = DatabaseConnection()
    repo = PartRepository(db)
    part_manager = PartManager(repo)
    part_ui = PartUI(part_manager)


    while True:
        active_account = account_system.main()

        car_repo = CarRepository(db)
        car_manager = CarManager(car_repo, active_account.user_id)
        maintenance_manager = MaintenanceManager(db, part_manager, car_manager)
        service = MaintenanceService(maintenance_manager)
        car_ui = CarUI(car_manager, active_account.user_id)

        maintenance_ui = MaintenanceUI(maintenance_manager,service,active_account.user_id)

        ui = VehicleUI(active_account.user_id, part_ui, car_ui, maintenance_ui, maintenance_manager, service)
        if active_account:
            logger.info(f"User {active_account.user_id} logged in")
            menu = Menu(ui)
            menu.main_menu()
        else:
            logger.info("No active account, exiting")
            break

if __name__ == "__main__":
    main()