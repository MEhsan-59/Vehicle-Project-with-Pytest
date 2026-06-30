#security.py
import hashlib

class SecurityHelper:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password, hashed_password):
        return SecurityHelper.hash_password(password) == hashed_password