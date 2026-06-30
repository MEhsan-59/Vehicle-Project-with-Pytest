#menu.py
import logging

class Menu:
    def __init__(self, ui=None):
        self.logger = logging.getLogger("menu")
        self.ui = ui
        self.logger.info("Menu system")

    def setting_menu(self) -> None:
        self.logger.debug("Entering setting menu")
        while True:
            print("\n" + "="*40)
            print("SETTINGS MENU")
            print("="*40)
            print("1. Part setting.")
            print("2. History setting.")
            print("B. Back to main menu")
            print("="*40)

            choice = input("Enter your choice: ").strip()
            self.logger.debug(f"Setting menu choice: {choice}")
            
            if choice == '1':
                self.logger.info("User selected Part settings")
                self.config_menu() 
            elif choice == '2':
                self.logger.info("User selected History settings")
                self.history_menu()
            elif choice.lower() == 'b':
                self.logger.info("Exiting settings menu")
                break
            else:
                self.logger.warning(f"Invalid setting menu choice: {choice}")
                print("Invalid choice try again.")

    def config_menu(self) -> None:
        self.logger.debug("Entering configuration menu")
        while True:
            print("\n" + "-"*30)
            print("PART CONFIGURATION")
            print("-"*30)
            print("1. Add part in config.")
            print("2. Update part in config.")
            print("3. Remove part from config.")
            print("B. Back to settings")
            print("-"*30)

            choice = input("Enter your choice: ").strip()
            self.logger.debug(f"Config menu choice: {choice}")
            
            if choice == '1':
                self.logger.info("User selected Add part")
                if self.ui:
                    self.ui.add_part()
            elif choice == '2':
                self.logger.info("User selected Update part")
                if self.ui:
                    self.ui.update_part()
            elif choice == '3':
                self.logger.info("User selected Remove part")
                if self.ui:
                    self.ui.remove_part()
            elif choice.lower() == 'b':
                self.logger.info("Exiting config menu")
                break
            else:
                self.logger.warning(f"Invalid config menu choice: {choice}")
                print("Invalid choice try again.")

    def history_menu(self) -> None:
        self.logger.debug("Entering history menu")
        while True:
            print("\n" + "-"*30)
            print("HISTORY SETTINGS")
            print("-"*30)
            print("1. View all history")
            print("2. View history by car number")
            print("3. View history by part name")
            print("B. Back to settings")
            print("-"*30)

            choice = input("Enter your choice: ").strip()
            self.logger.debug(f"History menu choice: {choice}")

            if choice == '1':
                self.logger.info("Viewing all history")
                if self.ui:
                    self.ui.view_all_history()
            elif choice == '2':
                car_num = input("Enter car number: ")
                self.logger.info(f"Viewing history for car: {car_num}")
                if self.ui:
                    self.ui.view_history_by_car(car_num)
            elif choice == '3':
                part_name = input("Enter part name: ")
                self.logger.info(f"Viewing history for part: {part_name}")
                if self.ui:
                    self.ui.view_history_by_part(part_name)
            elif choice.lower() == 'b':
                self.logger.info("Exiting history menu")
                break
            else:
                self.logger.warning(f"Invalid history menu choice: {choice}")
                print("Invalid choice try again.")
            input("\nPress Enter to continue...")

    def main_menu(self) -> None:
        self.logger.info("Main menu started")
        while True:
            print("\n" + "="*50)
            print("\n1. Add Car")
            print("2. Update Part")
            print("3. View Parts")
            print("4. Delete Car")
            print("5. Update daily km")
            print("6. Setting")
            print("b. Exit")
            print("="*50)

            choice = input("Enter your choice: ").strip()
            
            if choice.lower() == 'b':
                self.logger.info("User exiting application")
                print("\nThank you for using Vehicle Maintenance System!")
                break
            
            try:
                choice_num = int(choice)
            except ValueError:
                print("Invalid choice. Please enter a number or 'b' to exit.")
                continue
            
            if choice_num == 1:
                if self.ui:
                    self.ui.add_car()
                else:
                    print("UI not initialized")
            elif choice_num == 2:
                if self.ui:
                    self.ui.update_part()
                else:
                    print("UI not initialized")
            elif choice_num == 3:
                if self.ui:
                    self.ui.view_detail()
                else:
                    print("UI not initialized")
            elif choice_num == 4:
                if self.ui:
                    self.ui.delete_car()
                else:
                    print("UI not initialized")
            elif choice_num == 5:
                if self.ui:
                    self.ui.update_km()
                else:
                    print("UI not initialized")
            elif choice_num == 6:
                self.setting_menu()
            else:
                print("Invalid choice try again.")