# maintenance_manager.py
class MaintenanceManager:
    def __init__(self, db, part_manager, car_manager):
        self.db = db
        self.part_manager = part_manager
        self.car_manager = car_manager

    def update_part(self, car_no, part, changed_km, changed_date, user):
        return True, "Part updated"

    def get_vehicle_details(self, name, user):
        # Return a list of detail objects with attributes:
        # car_no, part_name, changed_km, next_changed_km, changed_date, next_changed_date
        return []

    def get_history(self, filter_type, value, user):
        # Return list of history objects
        return []