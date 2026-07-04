#utils.py
import datetime

class Utility:
    @staticmethod
    def add_months(date_obj, months) -> datetime.datetime:
        year = date_obj.year + (date_obj.month + months - 1) // 12
        month = (date_obj.month + months - 1) % 12 + 1
        day = date_obj.day

        while True:
            try:
                return datetime.datetime(year, month, day)
            except ValueError:
                day -= 1

    @staticmethod
    def get_valid_iso_date(prompt="تاریخ درج کریں (dd.mm.yyyy): ") -> str:
        allowed_formats = ["%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"]
        while True:
            user_input = input(prompt).strip()
            for fmt in allowed_formats:
                try:
                    date_obj = datetime.datetime.strptime(user_input, fmt)
                    return date_obj.date().isoformat()
                except ValueError:
                    continue
            print("❌ Invalid date format")

    @staticmethod
    def format_date(date_str):
        if not date_str:
            return "N/A"
        try:
            parts = date_str.split("-")
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        except (ValueError, IndexError):
            return date_str

    @staticmethod
    def format_timestamp(timestamp_str):
        try:
            dt = datetime.datetime.fromisoformat(timestamp_str)
            return dt.strftime("%d-%m-%Y %H:%M:%S")
        except Exception as e: 
            self.logger.error(f"Timestamp parse error: {e}")
            return timestamp_str
    
    @staticmethod
    def validate_int(
            prompt: str,
            min_val: int | None = None,
            max_val: int | None = None
        ) -> int | None:
        while True:
            choice = input(prompt)
            if not choice:
                print("Empty input is not allowed.")
                continue
            elif choice == 'b': return 'b'
            
            elif not choice.isdigit():
                print(f"Invalid input please inter in ({min} to {max})."); continue
            value = int(choice)
            if min is not None:
                if value < min:
                    print(f"Value must be greater then {min}. Please try again."); continue
        
            if max is not None:
                if value > max:
                    print(f"Value must be less then {max}. Please try again."); continue

            return int(choice)