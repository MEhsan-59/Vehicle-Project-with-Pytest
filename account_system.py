#account_system.py
from account_ui import AccountUI
from account_manager import AccountManager
from account_repository import AccountRepository

def main():
    account_repo = AccountRepository()
    account_manager = AccountManager(account_repo)
    account_ui = AccountUI(account_manager)
    active_account = account_repo.load_active_account()
    
    if not active_account:	
        while True:
            print("\n\nWELCOME TO VEHICLE MAINTENANCE APP")
            print("1. Create Account")
            print("2. Login Account")
            print("E. Exit.")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                account_ui.create_account()
            elif choice == '2':
                active_account = account_ui.login_account()
                if active_account:
                    return active_account
            elif choice.lower() == 'e':
                print("Goodbye!")
                exit()
            else:
                print("Invalid choice try again")
    else:
        print(f"Welcome back {active_account.user_id}")
        return active_account
    
    return None

if __name__ == '__main__':
    main()