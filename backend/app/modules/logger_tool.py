import os
import sys
from dotenv import load_dotenv, find_dotenv
import logging
import datetime

load_dotenv(find_dotenv())

# Define a global format string with alignment
LOG_FORMAT = "%(asctime)s %(levelname)-10s: %(filename)s > %(funcName)s >>> %(message)s"

# ANSI escape sequences for colors
class LogColors:
    """
    This class defines ANSI escape sequences for various log levels to colorize log output.
    """
    logging.debug("Setting up logger colors...")
    DARK_RED = '\033[31m'
    BRIGHT_RED = '\033[91m'
    ORANGE = '\033[33m'
    GOLD = '\033[93m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    DARKGREEN = '\033[32m'
    LIGHTGREEN = '\033[92m'
    LIGHTBLUE = '\033[94m'
    BLUE = '\033[94m'
    INDIGO = '\033[34m'
    VIOLET = '\033[35m'
    RESET = '\033[0m'
    WHITE = '\033[37m'
    BLACK = '\033[30m'

# Custom Formatter
class ColoredFormatter(logging.Formatter):
    """
    A custom formatter to add color to log messages for console output.
    """
    logging.debug("Setting up logger formatter...")
    COLORS = {
        logging.CRITICAL: LogColors.DARK_RED, # Level 50
        logging.ERROR: LogColors.BRIGHT_RED, # Level 40
        logging.WARNING: LogColors.ORANGE, # Level 30
        24: LogColors.GOLD, # SUCCESS level
        23: LogColors.WHITE, # APP level
        22: LogColors.ORANGE, # PROD level
        21: LogColors.YELLOW, # DATABASE level
        logging.INFO: LogColors.DARKGREEN, # Level 20
        logging.DEBUG: LogColors.LIGHTBLUE, # Level 10
        9: LogColors.LIGHTBLUE,  # TESTING level
        8: LogColors.BLUE,  # CHAT level
        7: LogColors.INDIGO,  # QUERY level
        5: LogColors.VIOLET,  # VARIABLES level
        1: LogColors.BLACK,  # PEDANTIC level
    }

    def format(self, record):
        record.filename = record.filename[:-3]  # Remove '.py' from filename
        # Use the global format string
        log_fmt = (self.COLORS.get(record.levelno) + LOG_FORMAT + LogColors.RESET)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Define custom logging levels
SUCCESS_LOG_LEVEL = 24
APP_LOG_LEVEL = 23
PROD_LOG_LEVEL = 22
DATABASE_LOG_LEVEL = 21
TESTING_LOG_LEVEL = 9
CHAT_LOG_LEVEL = 8
QUERY_LOG_LEVEL = 7
VARIABLES_LOG_LEVEL = 5
PEDANTIC_LOG_LEVEL = 1
logging.addLevelName(CHAT_LOG_LEVEL, "CHAT")
logging.addLevelName(VARIABLES_LOG_LEVEL, "VARIABLES")
logging.addLevelName(PEDANTIC_LOG_LEVEL, "PEDANTIC")
logging.addLevelName(PROD_LOG_LEVEL, "PROD")
logging.addLevelName(QUERY_LOG_LEVEL, "QUERY")
logging.addLevelName(DATABASE_LOG_LEVEL, "DATABASE")
logging.addLevelName(TESTING_LOG_LEVEL, "TESTING")
logging.addLevelName(APP_LOG_LEVEL, "APP")
logging.addLevelName(SUCCESS_LOG_LEVEL, "SUCCESS")

def chat(self, message, *args, **kws):
    if self.isEnabledFor(CHAT_LOG_LEVEL):
        self._log(CHAT_LOG_LEVEL, message, args, **kws)

def variables(self, message, *args, **kws):
    if self.isEnabledFor(VARIABLES_LOG_LEVEL):
        self._log(VARIABLES_LOG_LEVEL, message, args, **kws)

def pedantic(self, message, *args, **kws):
    if self.isEnabledFor(PEDANTIC_LOG_LEVEL):
        self._log(PEDANTIC_LOG_LEVEL, message, args, **kws)

def prod(self, message, *args, **kws):
    if self.isEnabledFor(PROD_LOG_LEVEL):
        self._log(PROD_LOG_LEVEL, message, args, **kws)

def query(self, message, *args, **kws):
    if self.isEnabledFor(QUERY_LOG_LEVEL):
        self._log(QUERY_LOG_LEVEL, message, args, **kws)
        
def database(self, message, *args, **kws):
    if self.isEnabledFor(DATABASE_LOG_LEVEL):
        self._log(DATABASE_LOG_LEVEL, message, args, **kws)
        
def testing(self, message, *args, **kws):
    if self.isEnabledFor(TESTING_LOG_LEVEL):
        self._log(TESTING_LOG_LEVEL, message, args, **kws)
        
def app(self, message, *args, **kws):
    if self.isEnabledFor(APP_LOG_LEVEL):
        self._log(APP_LOG_LEVEL, message, args, **kws)
        
def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LOG_LEVEL):
        self._log(SUCCESS_LOG_LEVEL, message, args, **kws)
        
logging.Logger.chat = chat
logging.Logger.prod = prod
logging.Logger.query = query
logging.Logger.variables = variables
logging.Logger.pedantic = pedantic
logging.Logger.database = database
logging.Logger.testing = testing
logging.Logger.app = app
logging.Logger.success = success

class FileFormatter(logging.Formatter):
    def format(self, record):
        # Use the global format string for file logging without ANSI color codes
        formatter = logging.Formatter(LOG_FORMAT)
        return formatter.format(record)

# Function to set an environment directory
def set_log_path(env_var):
    env_var_upper = env_var.upper()
    env_path = os.getenv(env_var_upper)
    
    if not os.path.exists(env_path):
        os.makedirs(env_path)
        
    return env_path

# Function to get a logger
def get_logger(name=None, log_level=None, log_path=None, log_file=None, delimiter='_'):
    """
    Creates and configures a logger with both console and file handlers.

    Args:
        name (str, optional): The name of the logger. Defaults to '__name__'.
        log_level (str, optional): The logging level. Defaults to 'INFO'.
        log_file (str, optional): The file name for the file handler. If None, no file handler is added.

    Returns:
        logging.Logger: The configured logger.
    """
    log_levels = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'CHAT': CHAT_LOG_LEVEL,
        'PROD': PROD_LOG_LEVEL,
        'QUERY': QUERY_LOG_LEVEL,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'VARIABLES': VARIABLES_LOG_LEVEL,
        'PEDANTIC': PEDANTIC_LOG_LEVEL,
        'DATABASE': DATABASE_LOG_LEVEL,
        'TESTING': TESTING_LOG_LEVEL,
        'APP': APP_LOG_LEVEL,
        'SUCCESS': SUCCESS_LOG_LEVEL
    }

    logger_name = name or __name__
    logger = logging.getLogger(logger_name)

    # Determine the desired level based on the log_level argument or existing logger level
    if log_level is not None:
        desired_level = log_levels.get(log_level, logging.INFO)
    else:
        # If no log_level provided and logger has a level set, use it; otherwise, default to INFO
        desired_level = logger.level if logger.level != 0 else logging.INFO

    # Set logger level
    logger.setLevel(desired_level)

    # Disable propagation to avoid duplicate logs in the root logger
    logger.propagate = False

    # Formatters
    console_formatter = ColoredFormatter(LOG_FORMAT)
    file_formatter = FileFormatter(LOG_FORMAT)

    # Check if the logger already has handlers
    if not logger.handlers:
        # Add console and file handlers if not present
        ch = logging.StreamHandler()
        ch.setLevel(desired_level)
        ch.setFormatter(console_formatter)
        logger.addHandler(ch)
        os.makedirs(log_path, exist_ok=True)
        log_file_path = os.path.join(log_path, f"{log_file}{delimiter}{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(desired_level)
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)
    else:
        # Log the types of existing handlers
        for handler in logger.handlers:
            handler.setLevel(desired_level)
            if isinstance(handler, logging.FileHandler):
                handler.setFormatter(file_formatter)
            elif isinstance(handler, logging.StreamHandler):
                handler.setFormatter(console_formatter)
    return logger


# function to get a list of all the loggers everywhere
def get_loggers():
    """
    Retrieves and returns a list of all logger instances currently in the Python logging manager.

    This function iterates through the logging manager's logger dictionary to collect all logger
    instances. It is useful for debugging purposes to see all the loggers that have been created
    in the application.

    Returns:
        list[logging.Logger]: A list of logger instances.
    """
    loggers = []
    for name in logging.Logger.manager.loggerDict:
        loggers.append(logging.getLogger(name))
    return loggers
    return loggers