import sys
import os

# project root ko path mein add karo taake imports kaam karein
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from account_repository import AccountRepository
from db_connection import DatabaseConnection
from part_repository import PartRepository
from car_repository import CarRepository


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
