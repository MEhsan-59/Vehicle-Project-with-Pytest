#account_manager.py
import security

class AccountManager:
    def __init__(self, repo):
        self.repo = repo
        
    def create_account(self, user_id, password):
        verify = self.repo.check_account(user_id)
        if verify:
            return False, "Account already exists"
        else:
            hashed_password = security.SecurityHelper.hash_password(password)
            self.repo.save_account(user_id, hashed_password)
            return True, "Account successfully created"
    
    def login_account(self, user_id, password):
        verify = self.repo.check_account(user_id)
        if not verify:
            return False, "Account does not exist."
        if not security.SecurityHelper.verify_password(password, verify.password):
            return False, "Invalid password."
        self.insert_active_account(user_id, verify.password)
        return True, verify

    def insert_active_account(self, user_id, password):
        return self.repo.insert_active_account(user_id, password)