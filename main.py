# main.py
from user_interface import PartUI, CarUI, MaintenanceUI
from db_connection import DatabaseConnection
from part_repository import PartRepository
from car_repository import CarRepository
from maintenance_repository import MaintenanceRepository
from service import MaintenanceService
from logger_setup import setup_logger
from part_manager import PartManager
from car_manager import CarManager
from maintenance_manager import MaintenanceManager
from menu import Menu
import logging
import account_system
from vehicle_ui import VehicleUI

def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Program started")

    while True:
        active_account = account_system.main()
        if active_account:
            active_user = active_account.user_id
            logger.info(f"User {active_user} logged in")

            db = DatabaseConnection()

            # Part subsystem
            part_repo = PartRepository(db)
            part_manager = PartManager(part_repo)
            part_ui = PartUI(part_manager)

            # Car subsystem
            car_repo = CarRepository(db)
            car_manager = CarManager(car_repo, active_user)
            car_ui = CarUI(car_manager, active_user)

            # Maintenance subsystem
            maintenance_repo = MaintenanceRepository(db)
            maintenance_manager = MaintenanceManager(car_repo, maintenance_repo,part_manager)
            maintenance_service = MaintenanceService(maintenance_manager)
            maintenance_ui = MaintenanceUI(maintenance_manager, maintenance_service, active_user)

            # Combined UI – note the correct order:
            vehicle_ui = VehicleUI(
                active_user=active_user,
                part_ui=part_ui,
                car_ui=car_ui,
                maintenance_ui=maintenance_ui,
                maintenance_manager=maintenance_manager,
                service=maintenance_service
            )

            menu = Menu(vehicle_ui)
            menu.main_menu()
        else:
            logger.info("No active account, exiting")
            break

if __name__ == "__main__":
    main()