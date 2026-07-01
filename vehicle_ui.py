# vehicle_ui.py
class VehicleUI:
    def __init__(self, active_user, part_ui, car_ui, maintenance_ui,
                 maintenance_manager, service):
        self.active_user = active_user
        self.part_ui = part_ui
        self.car_ui = car_ui
        self.maintenance_ui = maintenance_ui
        self.maintenance_manager = maintenance_manager
        self.service = service

        self._check_expiry()

    def _check_expiry(self):
        details = self.maintenance_manager.get_vehicle_details("", self.active_user)
        for detail in details:
            status = self.service.get_expiry_status(detail)
            if status:
                print(status)

    # Part configuration methods
    def add_part_config(self, status="add"):
        self.part_ui.add_part_config(status)

    def remove_part_config(self):
        self.part_ui.remove_part_config()

    # Car methods
    def add_car(self):
        self.car_ui.add_car()

    def delete_car(self):
        self.car_ui.delete_car()

    def update_km(self):
        self.car_ui.update_km()

    # Maintenance methods
    def update_part(self):
        self.maintenance_ui.update_part()

    def view_detail(self):
        self.maintenance_ui.view_detail()

    def show_history(self, filter_type='all', value=''):
        self.maintenance_ui.show_history(filter_type, value)