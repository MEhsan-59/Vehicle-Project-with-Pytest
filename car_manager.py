#car_manager.py
import sqlite3
from models import Vehicle
from car_repository import CarRepository
import logging

class CarManager:
    def __init__(self, car_repo: CarRepository, active_user):
        self.car_repo = car_repo
        self.active_user = active_user
        self.logger = logging.getLogger("car_manager")
        self.vehicles_dict = self._load_as_dict()

    def _load_as_dict(self) -> dict[str, Vehicle]:
        vehicles = {v.car_no: v for v in self.car_repo.load_all(self.active_user)}
        self.logger.info(f"Loaded {len(vehicles)} vehicles for user {self.active_user}")
        return vehicles

    def get_vehicle_from_cache(self, car_no: str) -> Vehicle | None:
        return self.vehicles_dict.get(car_no)

    def add_car(self, car_no: str, model: str, company: str, km: str, active_user: str) -> tuple[bool, str]:
        if not km.isdigit():
            return False, "KM must be numeric"

        vehicle = Vehicle(id=None, car_no=car_no, model=model, company=company, onground_km=int(km), active_user=active_user)
        try:
            vehicle_id = self.car_repo.insert(vehicle)
            vehicle.id = vehicle_id
            self.vehicles_dict[car_no] = vehicle
            self.logger.info(f"Car added: {car_no}")
            return True, "Car added successfully"
        except sqlite3.IntegrityError:
            self.logger.debug(f"Duplicate car: {car_no}")
            return False, "Car already exists"

    def delete_car(self, car_no: str, active_user: str) -> tuple[bool, str]:
        vehicle = self.vehicles_dict.get(car_no)
        if not vehicle or vehicle.active_user != active_user:
            return False, f"Car {car_no} not found"

        self.car_repo.delete(vehicle)
        del self.vehicles_dict[car_no]
        self.logger.info(f"Car deleted: {car_no}")
        return True, f"Car {car_no} successfully deleted"

    def update_km(self, car_no: str, km: int, active_user: str) -> tuple[bool, str]:
        vehicle = self.car_repo.get_by_car_no(car_no, active_user)
        if not vehicle:
            return False, f"Car {car_no} not found"
        if vehicle.onground_km > km:
            return False, f"Onground km must be grater then old km {vehicle.onground_km}"
        
        old_km = vehicle.onground_km
        vehicle.onground_km = km
        self.car_repo.update_km(vehicle)
        self.vehicles_dict[car_no] = vehicle
        self.logger.info(f"KM updated for {car_no}: {old_km} → {km}")
        return True, "Onground km successfully updated"