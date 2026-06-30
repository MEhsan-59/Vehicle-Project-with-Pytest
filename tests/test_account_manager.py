from unittest.mock import MagicMock
from account_manager import AccountManager
from account_model import Model
import security


def make_fake_account(user_id="ahsan", raw_password="pass123"):
    hashed = security.SecurityHelper.hash_password(raw_password)
    return Model(1, user_id, hashed, "01.01.2026 10:00:00", 5000)


def test_create_account_success():
    repo = MagicMock()
    repo.check_account.return_value = None  # account abhi exist nahi karta
    manager = AccountManager(repo)

    success, message = manager.create_account("ahsan", "pass123")

    assert success is True
    assert message == "Account successfully created"
    repo.save_account.assert_called_once()
    # ensure password jo save hua wo hashed ho, plain text na ho
    saved_args = repo.save_account.call_args[0]
    assert saved_args[1] != "pass123"


def test_create_account_already_exists():
    repo = MagicMock()
    repo.check_account.return_value = make_fake_account()
    manager = AccountManager(repo)

    success, message = manager.create_account("ahsan", "pass123")

    assert success is False
    assert message == "Account already exists"
    repo.save_account.assert_not_called()


def test_login_account_success():
    repo = MagicMock()
    fake_account = make_fake_account(raw_password="pass123")
    repo.check_account.return_value = fake_account
    manager = AccountManager(repo)

    success, result = manager.login_account("ahsan", "pass123")

    assert success is True
    assert result is fake_account
    repo.insert_active_account.assert_called_once_with("ahsan", fake_account.password)


def test_login_account_wrong_password():
    repo = MagicMock()
    fake_account = make_fake_account(raw_password="pass123")
    repo.check_account.return_value = fake_account
    manager = AccountManager(repo)

    success, message = manager.login_account("ahsan", "wrongpass")

    assert success is False
    assert message == "Invalid password."
    repo.insert_active_account.assert_not_called()


def test_login_account_does_not_exist():
    repo = MagicMock()
    repo.check_account.return_value = None
    manager = AccountManager(repo)

    success, message = manager.login_account("nouser", "pass123")

    assert success is False
    assert message == "Account does not exist."
