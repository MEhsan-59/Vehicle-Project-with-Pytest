# models.py
class PartConfig:
    def __init__(self, id, part, km_life, month_life, km_limit, day_limit):
        self.id = id
        self.part = part
        self.km_life = km_life
        self.month_life = month_life
        self.km_limit = km_limit
        self.day_limit = day_limit

    def __repr__(self):
        return f"Part : {self.part}: km_life={self.km_life}, month_life={self.month_life}"

class Vehicle:
    def __init__(self, id, car_no, model, company, onground_km, active_user):
        self.id = id
        self.car_no = car_no
        self.model = model
        self.company = company
        self.onground_km = onground_km
        self.active_user = active_user

    def __str__(self):
        return f"{self.car_no} - {self.model} ({self.company}) - {self.onground_km}km"

    def __repr__(self):
        return f"Vehicle(id={self.id}, car_no='{self.car_no}', model='{self.model}')"


class MaintenanceRecord:
    def __init__(self, id, vehicle_id, part_id, changed_km, next_changed_km, changed_date, next_changed_date):
        self.id = id
        self.vehicle_id = vehicle_id
        self.part_id = part_id
        self.changed_km = changed_km
        self.next_changed_km = next_changed_km
        self.changed_date = changed_date
        self.next_changed_date = next_changed_date

    def __str__(self):
        return f"Maintenance at {self.changed_km}km (Next: {self.next_changed_km}km)"

    def km_remaining(self, current_km):
        return self.next_changed_km - current_km

    def is_overdue_by_km(self, current_km):
        return current_km > self.next_changed_km



class VehicleMaintenanceDetail:
    def __init__(self, vehicle_id, car_no, model, company, onground_km,
                 part_name, changed_km, next_changed_km, changed_date, next_changed_date):
        self.vehicle_id = vehicle_id
        self.car_no = car_no
        self.model = model
        self.company = company
        self.onground_km = onground_km
        self.part_name = part_name
        self.changed_km = changed_km
        self.next_changed_km = next_changed_km
        self.changed_date = changed_date
        self.next_changed_date = next_changed_date

    def __str__(self):
        return f"{self.car_no} - {self.part_name}: {self.changed_km}km → {self.next_changed_km}km"

    def km_remaining(self):
        return self.next_changed_km - self.onground_km