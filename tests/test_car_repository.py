import sqlite3
import pytest
from models import Vehicle


def test_create_table_runs_without_error(car_repo):
    assert car_repo is not None


def test_insert_and_get_by_car_no(car_repo):
    vehicle = Vehicle(id=None, car_no="ABC123", model="Corolla",
                       company="Toyota", onground_km=1000, active_user="ahsan")

    vehicle_id = car_repo.insert(vehicle)

    assert vehicle_id is not None
    loaded = car_repo.get_by_car_no("ABC123", "ahsan")
    assert loaded is not None
    assert loaded.model == "Corolla"
    assert loaded.company == "Toyota"
    assert loaded.onground_km == 1000


def test_get_by_car_no_not_found(car_repo):
    assert car_repo.get_by_car_no("XYZ999", "ahsan") is None


def test_get_by_car_no_wrong_user_returns_none(car_repo):
    vehicle = Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan")
    car_repo.insert(vehicle)

    assert car_repo.get_by_car_no("ABC123", "other_user") is None


def test_load_all_filters_by_active_user(car_repo):
    car_repo.insert(Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan"))
    car_repo.insert(Vehicle(None, "XYZ999", "Civic", "Honda", 500, "other_user"))

    vehicles = car_repo.load_all("ahsan")

    assert len(vehicles) == 1
    assert vehicles[0].car_no == "ABC123"


def test_update_km_persists_change(car_repo):
    vehicle = Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan")
    vehicle.id = car_repo.insert(vehicle)

    vehicle.onground_km = 2000
    car_repo.update_km(vehicle)

    loaded = car_repo.get_by_car_no("ABC123", "ahsan")
    assert loaded.onground_km == 2000


def test_delete_removes_vehicle(car_repo):
    vehicle = Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan")
    vehicle.id = car_repo.insert(vehicle)

    car_repo.delete(vehicle)

    assert car_repo.get_by_car_no("ABC123", "ahsan") is None


def test_insert_duplicate_car_no_raises_integrity_error(car_repo):
    car_repo.insert(Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan"))

    with pytest.raises(sqlite3.IntegrityError):
        car_repo.insert(Vehicle(None, "ABC123", "Civic", "Honda", 500, "ahsan"))


def test_get_ongkm_by_car_id_returns_km(car_repo):
    vehicle = Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan")
    vehicle_id = car_repo.insert(vehicle)

    km = car_repo.get_ongkm_by_car_id(vehicle_id, "ahsan")

    assert km == 1000


def test_get_ongkm_by_car_id_not_found_returns_none(car_repo):
    assert car_repo.get_ongkm_by_car_id(999, "ahsan") is None
