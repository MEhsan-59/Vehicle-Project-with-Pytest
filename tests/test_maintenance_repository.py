import sqlite3
import pytest
from models import MaintenanceRecord, Vehicle, PartConfig


def make_record(vehicle_id, part_id, changed_km=5000, next_changed_km=10000,
                 changed_date="2026-01-01", next_changed_date="2026-07-01"):
    return MaintenanceRecord(
        id=None,
        vehicle_id=vehicle_id,
        part_id=part_id,
        changed_km=changed_km,
        next_changed_km=next_changed_km,
        changed_date=changed_date,
        next_changed_date=next_changed_date,
    )


def test_create_table_runs_without_error(maintenance_repo):
    assert maintenance_repo is not None


def test_get_record_not_found(maintenance_repo):
    assert maintenance_repo.get_record(1, 1) is None


def test_upsert_inserts_new_record(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part

    maintenance_repo.upsert(make_record(vehicle_id, part_id))

    saved = maintenance_repo.get_record(vehicle_id, part_id)
    assert saved is not None
    assert saved.changed_km == 5000
    assert saved.next_changed_km == 10000
    assert saved.changed_date == "2026-01-01"
    assert saved.next_changed_date == "2026-07-01"


def test_upsert_updates_existing_record_on_conflict(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id, changed_km=5000))

    maintenance_repo.upsert(make_record(
        vehicle_id, part_id, changed_km=15000, next_changed_km=20000,
        changed_date="2026-08-01", next_changed_date="2027-02-01"
    ))

    updated = maintenance_repo.get_record(vehicle_id, part_id)
    assert updated.changed_km == 15000
    assert updated.next_changed_km == 20000
    assert updated.changed_date == "2026-08-01"
    assert updated.next_changed_date == "2027-02-01"


def test_upsert_does_not_create_duplicate_rows_on_conflict(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id, changed_km=5000))
    maintenance_repo.upsert(make_record(vehicle_id, part_id, changed_km=6000))

    details = maintenance_repo.get_details("", "ahsan")
    matching = [d for d in details if d.car_no == "ABC123"]
    assert len(matching) == 1


def test_upsert_with_unknown_vehicle_raises_integrity_error(maintenance_repo, seeded_vehicle_and_part):
    _, part_id = seeded_vehicle_and_part

    with pytest.raises(sqlite3.IntegrityError):
        maintenance_repo.upsert(make_record(vehicle_id=9999, part_id=part_id))


def test_upsert_with_unknown_part_raises_integrity_error(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, _ = seeded_vehicle_and_part

    with pytest.raises(sqlite3.IntegrityError):
        maintenance_repo.upsert(make_record(vehicle_id=vehicle_id, part_id=9999))


def test_get_details_matches_car_no_keyword(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id))

    details = maintenance_repo.get_details("ABC", "ahsan")

    assert len(details) == 1
    assert details[0].car_no == "ABC123"
    assert details[0].part_name == "oil filter"


def test_get_details_matches_part_keyword(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id))

    details = maintenance_repo.get_details("oil", "ahsan")

    assert len(details) == 1
    assert details[0].part_name == "oil filter"


def test_get_details_empty_keyword_returns_all_for_user(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id))

    details = maintenance_repo.get_details("", "ahsan")

    assert len(details) == 1


def test_get_details_no_match_returns_empty_list(maintenance_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id))

    details = maintenance_repo.get_details("nonexistent", "ahsan")

    assert details == []


def test_get_details_filters_by_active_user(maintenance_repo, car_repo, part_repo):
    v1 = car_repo.insert(Vehicle(None, "ABC123", "Corolla", "Toyota", 1000, "ahsan"))
    v2 = car_repo.insert(Vehicle(None, "XYZ999", "Civic", "Honda", 500, "other_user"))
    part_config = PartConfig(None, "oil filter", 5000, 6, 200, 15)
    part_repo.save(part_config)

    maintenance_repo.upsert(make_record(v1, part_config.id))
    maintenance_repo.upsert(make_record(v2, part_config.id))

    details = maintenance_repo.get_details("", "ahsan")

    assert len(details) == 1
    assert details[0].car_no == "ABC123"


def test_get_details_orders_by_car_no(maintenance_repo, car_repo, part_repo):
    part_config = PartConfig(None, "oil filter", 5000, 6, 200, 15)
    part_repo.save(part_config)

    v_b = car_repo.insert(Vehicle(None, "BBB222", "Civic", "Honda", 500, "ahsan"))
    v_a = car_repo.insert(Vehicle(None, "AAA111", "Corolla", "Toyota", 1000, "ahsan"))

    maintenance_repo.upsert(make_record(v_b, part_config.id))
    maintenance_repo.upsert(make_record(v_a, part_config.id))

    details = maintenance_repo.get_details("", "ahsan")

    assert [d.car_no for d in details] == ["AAA111", "BBB222"]


def test_deleting_vehicle_cascades_to_maintenance(maintenance_repo, car_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id))

    vehicle = car_repo.get_by_car_no("ABC123", "ahsan")
    car_repo.delete(vehicle)

    assert maintenance_repo.get_record(vehicle_id, part_id) is None


def test_deleting_part_config_cascades_to_maintenance(maintenance_repo, part_repo, seeded_vehicle_and_part):
    vehicle_id, part_id = seeded_vehicle_and_part
    maintenance_repo.upsert(make_record(vehicle_id, part_id))

    part_config = part_repo.get_by_name("oil filter")
    part_repo.delete(part_config)

    assert maintenance_repo.get_record(vehicle_id, part_id) is None
