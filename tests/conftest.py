import sys
import os

# project root ko path mein add karo taake imports kaam karein
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from account_repository import AccountRepository
from db_connection import DatabaseConnection
from part_repository import PartRepository
from car_repository import CarRepository
from maintenance_repository import MaintenanceRepository
from models import Vehicle, PartConfig

@pytest.fixture
def repo(tmp_path, monkeypatch):
    """
    Har test ke liye nayi, temporary Bank.db file deta hai,
    taake asal Bank.db kabhi touch na ho.
    """
    monkeypatch.chdir(tmp_path)
    return AccountRepository()


@pytest.fixture
def db(tmp_path, monkeypatch):
    """
    Har test ke liye nayi, temporary sqlite db deta hai,
    taake asal Vehicle_app.db kabhi touch na ho.
    """
    monkeypatch.chdir(tmp_path)
    return DatabaseConnection(db_name="test_vehicle.db")


@pytest.fixture
def part_repo(db):
    """PartRepository backed by the temp db above."""
    return PartRepository(db)


@pytest.fixture
def car_repo(db):
    """CarRepository backed by the temp db above."""
    return CarRepository(db)
    
@pytest.fixture
def maintenance_repo(db, car_repo, part_repo):
    """
    MaintenanceRepository backed by the temp db above.
    Depends on car_repo/part_repo so that the 'vehicles' and 'config'
    tables (referenced by maintenance's FOREIGN KEYs) exist first.
    """
    return MaintenanceRepository(db)


@pytest.fixture
def seeded_vehicle_and_part(car_repo, part_repo):
    """
    A ready-made vehicle + part config, so maintenance tests don't
    have to repeat this setup. Returns (vehicle_id, part_id).
    """
    vehicle_id = car_repo.insert(
        Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan")
    )
    part_config = PartConfig(None, "oil filter", 5000, 6, 200, 15)
    part_repo.save(part_config)
    return vehicle_id, part_config.id