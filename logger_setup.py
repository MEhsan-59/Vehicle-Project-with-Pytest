#logger_setup.py
import logging

_logging_configured = False

def setup_logger():
    global _logging_configured
    if _logging_configured:
        return

    logging.basicConfig(level=logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s : %(name)s : %(levelname)s : %(message)s")
    file_handler.setFormatter(file_formatter)

    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)
    
    _logging_configured = True
    logging.info("LOGGING SYSTEM INITIALIZED.")