from unittest.mock import MagicMock
from part_manager import PartManager
from models import PartConfig


def make_fake_part(part_id=1, part="oil filter", km_life=5000,
                    month_life=6, km_limit=200, day_limit=15):
    return PartConfig(part_id, part, km_life, month_life, km_limit, day_limit)


def test_load_as_dict_on_init():
    repo = MagicMock()
    repo.load_all.return_value = [make_fake_part()]

    manager = PartManager(repo)

    assert manager.part_exists("oil filter") is True
    assert manager.get_part_config("oil filter").km_life == 5000


def test_get_part_config_not_found():
    repo = MagicMock()
    repo.load_all.return_value = []
    manager = PartManager(repo)

    assert manager.get_part_config("brake pad") is None


def test_part_exists_false_for_unknown_part():
    repo = MagicMock()
    repo.load_all.return_value = []
    manager = PartManager(repo)

    assert manager.part_exists("brake pad") is False


def test_save_part_config_adds_new_part():
    repo = MagicMock()
    repo.load_all.return_value = []
    repo.get_by_name.return_value = None
    manager = PartManager(repo)

    manager.save_part_config("brake pad", 3000, 4, 100, 10)

    repo.save.assert_called_once()
    assert manager.part_exists("brake pad") is True

    saved_config = manager.get_part_config("brake pad")
    assert saved_config.km_life == 3000
    assert saved_config.month_life == 4
    assert saved_config.km_limit == 100
    assert saved_config.day_limit == 10


def test_save_part_config_updates_existing_part():
    repo = MagicMock()
    existing = make_fake_part()
    repo.load_all.return_value = [existing]
    repo.get_by_name.return_value = existing
    manager = PartManager(repo)

    manager.save_part_config("oil filter", 7000, 8, 250, 20)

    repo.save.assert_called_once()
    updated = manager.get_part_config("oil filter")
    assert updated.km_life == 7000
    assert updated.month_life == 8
    assert updated.km_limit == 250
    assert updated.day_limit == 20
    # id should be preserved on update, not reset
    assert updated.id == existing.id


def test_delete_part_config_removes_existing_part():
    repo = MagicMock()
    existing = make_fake_part(part_id=1)
    repo.load_all.return_value = [existing]
    manager = PartManager(repo)

    manager.delete_part_config(1)

    repo.delete.assert_called_once_with(existing)
    assert manager.part_exists("oil filter") is False


def test_delete_part_config_nonexistent_id_does_nothing():
    repo = MagicMock()
    existing = make_fake_part(part_id=1)
    repo.load_all.return_value = [existing]
    manager = PartManager(repo)

    manager.delete_part_config(999)

    repo.delete.assert_not_called()
    assert manager.part_exists("oil filter") is True
