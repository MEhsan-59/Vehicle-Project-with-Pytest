# utils.py
import datetime

class Utility:
    @staticmethod
    def get_valid_iso_date(prompt):
        """Prompt for a date in ISO format (YYYY-MM-DD) and return as string."""
        while True:
            date_str = input(prompt).strip()
            if not date_str:
                print("Date cannot be empty.")
                continue
            try:
                # Validate format
                datetime.datetime.fromisoformat(date_str)
                return date_str
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    @staticmethod
    def format_date(date_obj):
        """Format a datetime object as YYYY-MM-DD."""
        if isinstance(date_obj, datetime.datetime):
            return date_obj.strftime("%Y-%m-%d")
        return str(date_obj)

    @staticmethod
    def format_timestamp(timestamp):
        """Format a datetime object as YYYY-MM-DD HH:MM:SS."""
        if isinstance(timestamp, datetime.datetime):
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return str(timestamp)