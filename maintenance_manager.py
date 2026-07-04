#maintenance_manager.py
import datetime
from models import MaintenanceRecord
from car_repository import CarRepository
from maintenance_repository import MaintenanceRepository
from part_manager import PartManager
from utils import Utility
import logging

class MaintenanceManager:
    def __init__(self, car_repo: CarRepository, maintenance_repo: MaintenanceRepository,
                 part_manager: PartManager):
        self.car_repo = car_repo
        self.maintenance_repo = maintenance_repo
        self.part_manager = part_manager
        self.logger = logging.getLogger("maintenance_manager")

    def update_part(self, car_no: str, part: str, new_change_km: int,
                    new_change_date: datetime.datetime, active_user: str) -> tuple[bool, str]:
        vehicle = self.car_repo.get_by_car_no(car_no, active_user)
        if not vehicle:
            return False, "Car not found"

        part_config = self.part_manager.get_part_config(part)
        if not part_config:
            return False, "Invalid part"

        if new_change_date > datetime.datetime.now():
            return False, "Future date not allowed."

        existing = self.maintenance_repo.get_record(vehicle.id, part_config.id)
        is_new = existing is None
        ongkm = self.car_repo.get_by_car_no(car_no, active_user).onground_km
        if new_change_km > ongkm:
            return False, "New change Km must less then on ground km"
        if existing:
            if new_change_km > ongkm:
                return False, f"Change KM must less then On ground KM"
        
        next_km = new_change_km + part_config.km_life
        next_date = Utility.add_months(new_change_date, part_config.month_life)

        maintenance = MaintenanceRecord(
            id=existing.id if existing else None,
            vehicle_id=vehicle.id,
            part_id=part_config.id,
            changed_km=new_change_km,
            next_changed_km=next_km,
            changed_date=new_change_date.date().isoformat(),
            next_changed_date=next_date.date().isoformat()
        )
        self.maintenance_repo.upsert(maintenance)

        self.logger.info(f"{part} {'added' if is_new else 'updated'} for {car_no}")
        return True, f"{part} updated successfully"

    def get_vehicle_details(self, keyword: str, active_user: str) -> list[VehicleMaintenanceDetail]:
        results = self.maintenance_repo.get_details(keyword, active_user)
        self.logger.debug(f"Found {len(results)} vehicles for '{keyword}'")
        return results