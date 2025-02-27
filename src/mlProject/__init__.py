import os      # Provides functions for interacting with the operating system
import sys     # Provides access to system-specific parameters and functions
import logging # Standard library module for logging events and messages

# Define a logging format that includes the time, log level, module, and message
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Specify the directory where logs will be stored
log_dir = "logs"

# Construct the full path to the log file by joining the directory and the log filename
log_filepath = os.path.join(log_dir, "running_logs.log")

# Ensure the log directory exists; create it if it doesn't
os.makedirs(log_dir, exist_ok=True)

# Configure the logging system with:
# - INFO level (i.e., all messages with level INFO and above will be logged)
# - The defined logging format (logging_str)
# - Two handlers: one for writing logs to a file and another for outputting logs to the console
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),  # Logs messages to the file specified by log_filepath
        logging.StreamHandler(sys.stdout)   # Also logs messages to the standard output (console)
    ]
)

# Create a named logger "mlProjectLogger" that can be used across the project for logging
logger = logging.getLogger("mlProjectLogger")
