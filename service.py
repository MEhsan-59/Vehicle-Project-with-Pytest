# service.py
class MaintenanceService:
    def __init__(self, maintenance_manager):
        self.manager = maintenance_manager

    def get_expiry_status(self, detail):
        # Return a string or None
        return None