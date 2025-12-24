# Standard Library
import logging
# MY Code
from core.my_logging.auto_log import AutoLog
from core.my_logging.main_logger import MainLogger

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# The "my_logging.custom_formatter.py" and "my_logging.helper.py" modules are only used in
# the MainLogger class, so I don't make them available outside this package.
__all__ = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "AutoLog", "MainLogger"]
