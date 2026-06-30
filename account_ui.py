#account_ui.py
class AccountUI:
    def __init__(self, manager):
        self.manager = manager
    
    def create_account(self):
        while True:
            id = input("Enter your id (b to back): ").strip()
            if id.lower() == 'b':
                break
            password = input("Enter your password: ").strip()
            
            if not id or not password:
                print("Empty input is not allowed.")
                continue
            status, msg = self.manager.create_account(id, password)
            print(msg)
            if status:
                break 
    
    def login_account(self):
        while True:
            id = input("Enter your id (b to back): ").strip()
            if id.lower() == 'b':
                break
            password = input("Enter your password: ").strip()
            
            if not id or not password:
                print("Empty input is not allowed.")
                continue
            status, account = self.manager.login_account(id, password)
            if not status:
                print(account)
                continue
            print("Account successfully logged in")
            return account 
        return None 

    def insert_active_account(self, user_id, password):
        return self.manager.insert_active_account(user_id, password)