from config import Config


def test_create_table_runs_without_error(repo):
    # constructor already calls create_table; agar koi error na aaye to pass
    assert repo is not None


def test_save_and_check_account(repo):
    repo.save_account("ahsan", "hashed_pw")
    account = repo.check_account("ahsan")

    assert account is not None
    assert account.user_id == "ahsan"
    assert account.password == "hashed_pw"
    assert account.balance == Config.DEFAULT_BALANCE


def test_check_account_not_found(repo):
    account = repo.check_account("no_such_user")
    assert account is None


def test_check_account_with_correct_password(repo):
    repo.save_account("ahsan", "hashed_pw")
    account = repo.check_account("ahsan", "hashed_pw")
    assert account is not None


def test_check_account_with_wrong_password(repo):
    repo.save_account("ahsan", "hashed_pw")
    account = repo.check_account("ahsan", "wrong_hash")
    assert account is None


def test_update_balance_increases_balance(repo):
    repo.save_account("ahsan", "hashed_pw")
    repo.update_balance("ahsan", 1000)

    account = repo.check_account("ahsan")
    assert account.balance == Config.DEFAULT_BALANCE + 1000


def test_insert_and_load_active_account(repo):
    repo.save_account("ahsan", "hashed_pw")
    repo.insert_active_account("ahsan", "hashed_pw")

    active = repo.load_active_account()
    assert active is not None
    assert active.user_id == "ahsan"


def test_load_active_account_when_none_saved(repo):
    active = repo.load_active_account()
    assert active is None
