#user_interface.py
from maintenance_manager import MaintenanceManager
from service import MaintenanceService
from part_manager import PartManager
from car_manager import CarManager
from utils import Utility
import datetime
import logging

class CarUI:
    def __init__(self, car_manager: CarManager | None, active_user: str):
        self.car_manager = car_manager
        self.active_user = active_user
        self.logger = logging.getLogger("car_ui")

    def add_car(self):
        car_no = input("Enter car number: ").upper()
        model = input("Enter model: ").title()
        company = input("Enter company: ").title()
        km = input("Enter on-ground km: ")

        success, msg = self.car_manager.add_car(car_no, model, company, km, self.active_user)
        if success:
            self.logger.info(f"User added car: {car_no}")
        print(msg)

    def delete_car(self):
        car_no = input("Enter car no to delete: ").upper()
        if input("Are you sure? (y/n): ").lower() != 'y':
            print("deletion aborted.")
            return

        success, msg = self.car_manager.delete_car(car_no, self.active_user)
        if success:
            self.logger.info(f"User deleted car: {car_no}")
        print(msg)

    def update_km(self):
        car_no = input("Enter car no to update km: ").upper()
        km = input("Enter your km to update: ")

        if not km.isdigit():
            print("Invalid km.")
            return

        success, msg = self.car_manager.update_km(car_no, int(km), self.active_user)
        if success:
            self.logger.info(f"User updated KM for {car_no} to {km}")
        print(msg)

class MaintenanceUI:
    def __init__(self, maintenance_manager: MaintenanceManager,
                 service: MaintenanceService, active_user: str):
        self.maintenance_manager = maintenance_manager
        self.service             = service
        self.active_user         = active_user

    def update_part(self):
        car_no     = input("Enter car number: ").upper()
        part       = input("Enter part name: ").lower()
        changed_km = input("Enter changed KM: ")

        if not changed_km.isdigit():
            print("KM must be numeric")
            return

        changed_date_str = Utility.get_valid_iso_date("Enter changed date: ")
        new_change_date     = datetime.datetime.fromisoformat(changed_date_str)

        success, msg = self.maintenance_manager.update_part(
            car_no, part, int(changed_km), new_change_date, self.active_user)
        print(msg)

    def view_detail(self):
        name    = input("Enter car number or part name: ")
        details = self.maintenance_manager.get_vehicle_details(name, self.active_user)

        if not details:
            print("No records found")
            return

        print("-" * 90)
        print(f"{'Car No':<10} | {'Part':<12} | {'Changed km':<10} | {'Next KM':<7} | "
              f"{'Changed date':<12} | {'Next Date':<12}")
        print("-" * 90)

        for d in details:
            print(f"{d.car_no:<10} | {d.part_name:<12} | {d.changed_km:<10} | "
                  f"{d.next_changed_km:<7} | {Utility.format_date(d.changed_date):<12} | "
                  f"{Utility.format_date(d.next_changed_date):<12}")

class PartUI:
    def __init__(self, part_manager: PartManager):
        self.part_manager = part_manager

    def add_part_config(self, status="add"):
        while True:
            part = input("Enter your part name (b to back): ").lower()
            if part == 'b':
                break

            exists = self.part_manager.part_exists(part)

            if status == 'add':
                if exists:
                    print(f"{part} already exists.")
                    if input("Do you want to update it (y/n): ").lower() != 'y':
                        continue
                    status = "Updated"
            else:
                if not exists:
                    print(f"{part} does not exist.")
                    if input("Do you want to add this part (y/n): ").lower() != 'y':
                        continue
                    status = "add"

            try:
                km_life    = int(input("Enter your km life: "))
                month_life = int(input("Enter your month life: "))
                km_limit   = int(input("Enter your km limit: "))
                day_limit  = int(input("Enter your day limit: "))
            except ValueError:
                print("Input must be numeric")
                continue

            self.part_manager.save_part_config(part, km_life, month_life, km_limit, day_limit)
            print(f"{part} {status} successful.")

    def remove_part_config(self):
        while True:
            print(self.part_manager.part_configs)
            for config in self.part_manager.part_configs.values():
                print(f"{config.id}. {config}")

            index = input("Enter part id to remove (b to back): ")
            if index.lower() == 'b':
                return
            if not index.isdigit():
                print("Index must be numeric")
                continue
            if input(f"Are you sure to delete part {index}? History will be deleted (y/n): ").lower() != 'y':
                continue

            self.part_manager.delete_part_config(int(index))
            print("Part removed successfully.")