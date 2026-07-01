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


