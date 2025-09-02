import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Formatters
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_STR = datetime.now().strftime("%Y-%m-%d")

# File paths
SIGNAL_LOG_FILE = os.path.join(LOG_DIR, f"signal_log_{DATE_STR}.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, f"error_log_{DATE_STR}.log")

# Signal logger
signal_logger = logging.getLogger("signal_logger")
signal_logger.setLevel(logging.INFO)
signal_handler = logging.FileHandler(SIGNAL_LOG_FILE)
signal_handler.setFormatter(logging.Formatter(LOG_FORMAT))
signal_logger.addHandler(signal_handler)

# Error logger
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(ERROR_LOG_FILE)
error_handler.setFormatter(logging.Formatter(LOG_FORMAT))
error_logger.addHandler(error_handler)

# Public functions
def log_signal(message):
    signal_logger.info(message)

def log_error(message):
    error_logger.error(message)
