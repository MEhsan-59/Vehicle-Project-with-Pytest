from security import SecurityHelper


def test_hash_password_returns_different_string():
    hashed = SecurityHelper.hash_password("mySecret123")
    assert hashed != "mySecret123"
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # sha256 hex digest length


def test_hash_password_is_deterministic():
    assert SecurityHelper.hash_password("abc") == SecurityHelper.hash_password("abc")


def test_verify_password_correct():
    hashed = SecurityHelper.hash_password("mySecret123")
    assert SecurityHelper.verify_password("mySecret123", hashed) is True


def test_verify_password_incorrect():
    hashed = SecurityHelper.hash_password("mySecret123")
    assert SecurityHelper.verify_password("wrongPassword", hashed) is False
