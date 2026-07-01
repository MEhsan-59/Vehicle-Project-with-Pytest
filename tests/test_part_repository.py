import sqlite3
import pytest
from models import PartConfig


def test_create_table_runs_without_error(part_repo):
    # constructor already calls _create_table; agar koi error na aaye to pass
    assert part_repo is not None


def test_save_new_part_config_and_load(part_repo):
    config = PartConfig(id=None, part="oil filter", km_life=5000,
                         month_life=6, km_limit=200, day_limit=15)

    part_repo.save(config)

    assert config.id is not None
    loaded = part_repo.get_by_name("oil filter")
    assert loaded is not None
    assert loaded.part == "oil filter"
    assert loaded.km_life == 5000
    assert loaded.month_life == 6
    assert loaded.km_limit == 200
    assert loaded.day_limit == 15


def test_get_by_name_not_found(part_repo):
    assert part_repo.get_by_name("nonexistent") is None


def test_save_updates_existing_part_config(part_repo):
    config = PartConfig(id=None, part="oil filter", km_life=5000,
                         month_life=6, km_limit=200, day_limit=15)
    part_repo.save(config)
    original_id = config.id

    config.km_life = 8000
    config.month_life = 10
    part_repo.save(config)

    loaded = part_repo.get_by_name("oil filter")
    assert loaded.id == original_id
    assert loaded.km_life == 8000
    assert loaded.month_life == 10


def test_load_all_returns_all_configs(part_repo):
    part_repo.save(PartConfig(None, "oil filter", 5000, 6, 200, 15))
    part_repo.save(PartConfig(None, "brake pad", 3000, 4, 100, 10))

    all_configs = part_repo.load_all()
    parts = {c.part for c in all_configs}

    assert len(all_configs) == 2
    assert parts == {"oil filter", "brake pad"}


def test_delete_removes_part_config(part_repo):
    config = PartConfig(None, "oil filter", 5000, 6, 200, 15)
    part_repo.save(config)

    part_repo.delete(config)

    assert part_repo.get_by_name("oil filter") is None


def test_save_duplicate_part_name_raises_integrity_error(part_repo):
    part_repo.save(PartConfig(None, "oil filter", 5000, 6, 200, 15))

    with pytest.raises(sqlite3.IntegrityError):
        part_repo.save(PartConfig(None, "oil filter", 6000, 7, 220, 18))
