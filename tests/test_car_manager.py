from unittest.mock import MagicMock
import sqlite3
from car_manager import CarManager
from models import Vehicle


def make_fake_vehicle(car_no="ABC123", model="Corolla", company="Toyota",
                       onground_km=1000, active_user="ahsan", vehicle_id=1):
    return Vehicle(vehicle_id, car_no, model, company, onground_km, active_user)


def test_load_as_dict_on_init():
    repo = MagicMock()
    repo.load_all.return_value = [make_fake_vehicle()]

    manager = CarManager(repo, "ahsan")

    assert manager.get_vehicle_from_cache("ABC123") is not None


def test_get_vehicle_from_cache_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []
    manager = CarManager(repo, "ahsan")

    assert manager.get_vehicle_from_cache("XYZ999") is None


def test_add_car_success():
    repo = MagicMock()
    repo.load_all.return_value = []
    repo.insert.return_value = 1
    manager = CarManager(repo, "ahsan")

    success, msg = manager.add_car("ABC123", "Corolla", "Toyota", "1000", "ahsan")

    assert success is True
    assert msg == "Car added successfully"
    repo.insert.assert_called_once()
    assert manager.get_vehicle_from_cache("ABC123") is not None


def test_add_car_invalid_km():
    repo = MagicMock()
    repo.load_all.return_value = []
    manager = CarManager(repo, "ahsan")

    success, msg = manager.add_car("ABC123", "Corolla", "Toyota", "not_a_number", "ahsan")

    assert success is False
    assert msg == "KM must be numeric"
    repo.insert.assert_not_called()


def test_add_car_duplicate_car_no():
    repo = MagicMock()
    repo.load_all.return_value = []
    repo.insert.side_effect = sqlite3.IntegrityError
    manager = CarManager(repo, "ahsan")

    success, msg = manager.add_car("ABC123", "Corolla", "Toyota", "1000", "ahsan")

    assert success is False
    assert msg == "Car already exists"


def test_delete_car_success():
    repo = MagicMock()
    repo.load_all.return_value = [make_fake_vehicle()]
    manager = CarManager(repo, "ahsan")

    success, msg = manager.delete_car("ABC123", "ahsan")

    assert success is True
    assert msg == "Car ABC123 successfully deleted"
    repo.delete.assert_called_once()
    assert manager.get_vehicle_from_cache("ABC123") is None


def test_delete_car_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []
    manager = CarManager(repo, "ahsan")

    success, msg = manager.delete_car("XYZ999", "ahsan")

    assert success is False
    assert msg == "Car XYZ999 not found"
    repo.delete.assert_not_called()


def test_delete_car_wrong_user_rejected():
    repo = MagicMock()
    repo.load_all.return_value = [make_fake_vehicle(active_user="ahsan")]
    manager = CarManager(repo, "ahsan")

    success, msg = manager.delete_car("ABC123", "someone_else")

    assert success is False
    repo.delete.assert_not_called()


def test_update_km_success():
    repo = MagicMock()
    repo.load_all.return_value = []
    repo.get_by_car_no.return_value = make_fake_vehicle(onground_km=1000)
    manager = CarManager(repo, "ahsan")

    success, msg = manager.update_km("ABC123", 1500, "ahsan")

    assert success is True
    assert msg == "Onground km successfully updated"
    repo.update_km.assert_called_once()


def test_update_km_car_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []
    repo.get_by_car_no.return_value = None
    manager = CarManager(repo, "ahsan")

    success, msg = manager.update_km("XYZ999", 1500, "ahsan")

    assert success is False
    assert msg == "Car XYZ999 not found"
    repo.update_km.assert_not_called()


def test_update_km_lower_than_existing_rejected():
    repo = MagicMock()
    repo.load_all.return_value = []
    repo.get_by_car_no.return_value = make_fake_vehicle(onground_km=2000)
    manager = CarManager(repo, "ahsan")

    success, msg = manager.update_km("ABC123", 1000, "ahsan")

    assert success is False
    repo.update_km.assert_not_called()
