# Standard Library
import configparser
import logging
import logging.handlers
import os
import sys
import time
import typing

import Main
# MY Code
from core.config_reader import ConfigReader as CR
from core.my_logging.helper import LoggingHelper
from core.my_logging.custom_formatter import CustomFormatter

__initialized__ = False


class MainLogger(object):
	"""

	NOTES (in no particular order):
	1) UTF-8 will ensure proper encoding for non-English language characters.
	"""
	# utc_offset_pattern: str = r"^.+(?P<offset>[-+]\d{2}:\d{2})$"  # Regex also works.
	instance = None
	is_initialized = False
	# Uvicorn loggers
	uvicorn_access_logger: logging.Logger = None
	uvicorn_error_logger: logging.Logger = None
	# Standard settings for Formatter and file/stream handlers
	record_terminator = "\n"
	message_format = "%(asctime)s - %(levelname)s %(name)s\n%(message)s"
	date_format = "%Y-%m-%dT%H:%M:%S.%f"
	# Defaults
	default_log_level_main = logging.WARNING
	default_log_level_uvicorn = logging.INFO
	default_log_level_file_handler = logging.NOTSET
	default_log_level_stream_handler = logging.NOTSET
	default_log_level_name_main: str = LoggingHelper.get_level_name(default_log_level_main)
	default_log_level_name_uvicorn = LoggingHelper.get_level_name(default_log_level_uvicorn)
	default_log_level_file_handler_name = LoggingHelper.get_level_name(default_log_level_file_handler)
	default_log_level_stream_handler_name = LoggingHelper.get_level_name(default_log_level_stream_handler)
	emergency_log_file = "logs/emergency.log"  # In case something goes wrong during configuration
	default_log_file = "logs/main.log"
	default_encoding = "utf-8"
	default_rollover = "midnight"
	# Names
	main_logger_name: str = "MainLogger"
	file_handler_name: str = "FileHandler"
	stream_handler_name: str = "StdoutHandler"
	#
	pending_errors_to_report: dict[str, Exception] = dict()
	# TODO: Revisit this...maybe.
	# message_formats = {
	# 	"default": "%(asctime)s - %(levelname)s\n%(message)s",
	# 	"preferred": "%(asctime)s - [%(processName)s: %(process)d] %(levelname)s %(name)s\n%(message)s"
	# }
	# date_formats = {
	# 	"default": "%Y-%m-%dT%H:%M:%S.%f"
	# }

	def __new__(cls, init=False):
		"""

		NOTES (in no particular order):
		1) If the filename value passed to a FileHandler object refers to a file that doesn't exist,
		Python will create the file automatically.

		"""
		if cls.instance is None:
#			s = Main.args.s 
			instance: 'MainLogger' = super(MainLogger, cls).__new__(cls)
			instance.logger = logging.getLogger(cls.main_logger_name)
			instance.logger.setLevel(cls.default_log_level_main)

			# Make sure "logs" directory exists
			cls.make_sure_log_dir_exists(cls.emergency_log_file)

			default_formatter = CustomFormatter(fmt=cls.message_format, datefmt=cls.date_format)
			file_handler = cls.build_file_handler(
				cls.emergency_log_file, cls.default_encoding,
				cls.default_rollover, default_formatter
			)
			instance.logger.addHandler(file_handler)
			stdout_handler = cls.build_stream_handler(default_formatter)
			instance.logger.addHandler(stdout_handler)
			cls.instance = instance
			# Prepare Uvicorn loggers
			b_replace_file_handler: bool = False
			cls.uvicorn_access_logger = cls.set_uvicorn_logger(
				logging.getLogger("uvicorn.access"), cls.default_log_level_uvicorn,
				file_handler, b_replace_file_handler
			)
			cls.uvicorn_error_logger = cls.set_uvicorn_logger(
				logging.getLogger("uvicorn.error"), cls.default_log_level_uvicorn,
				file_handler, b_replace_file_handler
			)
			if init:
				cls.instance.initialize()
		return cls.instance

	@classmethod
	def initialize(cls):
		"""
		Try reading from the configuration file.

		NOTES (in no particular order):
		1) If the "s_rollover_when" value is invalid, the program will raise a built-in ValueError
		exception, which we catch and handle in "build_file_handler()".
		2) If the "s_encoding" value is invalid, the program will raise a built-in LookupError
		exception, which we catch and handle in "build_file_handler()".
		3) Issues with the "s_date_format" value should become apparent when reading the config
		file; the improperly written timestamps should speak for themselves.

		:return:
		"""
		if cls.is_initialized:
			print("already initialized.")
			return
		print("initializing...")
		t_config: tuple[int, int, int, int, str, str, str] = MainLogger.get_configuration()
		(i_level_main, i_level_uvicorn, i_level_file_handler, i_level_stream_handler,
				s_file_name, s_encoding, s_rollover_when) = t_config

		# Make sure new destination directory exists
		cls.make_sure_log_dir_exists(s_file_name)

		# Adjust MainLogger settings based on configuration settings
		new_formatter = CustomFormatter(fmt=cls.message_format, datefmt=cls.date_format)
		cls.instance.logger.setLevel(i_level_main)
		# Remove old file and stream handlers, replace with new ones
		cls.instance.logger.handlers.clear()
		file_handler = cls.build_file_handler(s_file_name, s_encoding, s_rollover_when, new_formatter, i_level_file_handler)
		cls.instance.logger.addHandler(file_handler)
		stdout_handler = cls.build_stream_handler(new_formatter, i_level_stream_handler)
		cls.instance.logger.addHandler(stdout_handler)
		# Modify existing Uvicorn Loggers
		b_replace_file_handler: bool = True
		cls.uvicorn_access_logger = cls.set_uvicorn_logger(
			cls.uvicorn_access_logger, i_level_uvicorn, file_handler, b_replace_file_handler
		)
		cls.uvicorn_error_logger = cls.set_uvicorn_logger(
			cls.uvicorn_error_logger, i_level_uvicorn, file_handler, b_replace_file_handler
		)
		# Prepare initial log message
		s_timezone: str = time.tzname[time.localtime().tm_isdst]
		offset_hours: float = -(time.timezone / (60 * 60))  # 3,600 seconds in hour
		cls.log(
			logging.INFO,
			lambda:
				f"Local time is {s_timezone} = UTC{offset_hours}\nLogging level: {LoggingHelper.get_level_name(i_level_main)}"
		)

		# Report exceptions that were caught during "post_new()", but not yet logged.
		for message, caught_exception in cls.pending_errors_to_report.items():
			cls.log_exception(message, caught_exception)
		cls.pending_errors_to_report.clear()
		print("initialized.")
		cls.is_initialized = True
		global __initialized__
		__initialized__ = True

	@classmethod
	def make_sure_log_dir_exists(cls, s_path: str) -> None:
		"""
		Before trying to open or save any log files, make sure the destination directory exists.

		NOTES (in no particular order):
		1) "os.path.split()" returns a tuple of 2 strings - head and tail. The "tail" is the last
		part of the path, the name of the file itself with extension. The "head" is the path of the
		file's home directory. Some examples:
			* If "s_path" = "logs/emergency.log"...
				head = "logs"
				tail = "emergency.log"
			* If "s_path" = "folder1/folder2/file.txt"...
				head = "folder1/folder2"
				tail = "file.txt"
			* If "s_path" = "/home/User/Desktop/file.txt"...
				head = "/home/User/Desktop"
				tail = "file.txt"

		:param s_path: String = String representation of path to log file; this path is relative to
		the root directory of the project

		:return: This method doesn't return anything.
		"""
		t_path_parts: tuple[str, str] = os.path.split(s_path)
		head, tail = t_path_parts
		if not os.path.isdir(head):
			os.makedirs(head)

	@classmethod
	def build_file_handler(
			cls, file_name: str, encoding: str, rollover_when: str,
			formatter: CustomFormatter, i_log_level: int = logging.NOTSET
	):
		""""""
		rollover_to_use: str = rollover_when
		encoding_to_use: str = encoding
		# file_handler: logging.handlers.TimedRotatingFileHandler | None = None
		while True:
			try:
				file_handler = logging.handlers.TimedRotatingFileHandler(filename=file_name, encoding=encoding_to_use, when=rollover_to_use)
				file_handler.set_name(cls.file_handler_name)
				file_handler.setFormatter(formatter)
				file_handler.setLevel(i_log_level)
				file_handler.terminator = cls.record_terminator
				return file_handler
				# break
			except LookupError as look_error:
				cls.pending_errors_to_report[f"Invalid encoding '{encoding}'"] = look_error
				encoding_to_use = cls.default_encoding
				continue
			except ValueError as val_error:
				cls.pending_errors_to_report[f"Invalid rollover '{rollover_when}'"] = val_error
				rollover_to_use = cls.default_rollover
				continue
		# return file_handler

	@classmethod
	def build_stream_handler(
			cls, formatter: CustomFormatter, i_log_level: int = logging.NOTSET
	) -> logging.StreamHandler:
		""""""
		stdout_handler = logging.StreamHandler(stream=sys.stdout)
		stdout_handler.set_name(cls.stream_handler_name)
		stdout_handler.setFormatter(formatter)
		stdout_handler.setLevel(i_log_level)
		stdout_handler.terminator = cls.record_terminator
		return stdout_handler

	@classmethod
	def set_uvicorn_logger(
			cls, logger: logging.Logger, i_log_level: int,
			file_handler: logging.handlers.TimedRotatingFileHandler, b_replace_file_handler: bool
	) -> logging.Logger:
		""""""
		logger.setLevel(i_log_level)
		if b_replace_file_handler:
			logger.handlers.clear()
		logger.addHandler(file_handler)
		return logger

	# TODO: Find better name for this method.
	@classmethod
	def try_translate_level_name_to_level_number(cls, s_level_name_from_config: str, i_default: int = logging.DEBUG) -> int:
		"""
		Handle repeated steps of examining and validating the log level.

		From the config file, we have a name. To set the log level, we need a number. Find the
		numeric value that corresponds to the log level name.

		The "logging" package has dictionaries to map levels to names, and vice versa. We use a
		copy of the level ==> name dictionary. We call the built-in "get()" method on that copy,
		which will return None if there's no such key in the dictionary.

		NOTES (in no particular order):
		1) As a courtesy, we accept "verbose" as a log level and translate it into the "DEBUG"
		value that the "logging" package would recognize.
		"""
		if s_level_name_from_config.lower() == "verbose":
			i_log_level = logging.DEBUG
		else:
			i_log_level: int = LoggingHelper.get_level_from_name(s_level_name_from_config.upper())
			if i_log_level is None:
				i_log_level = i_default
				cls.instance.log(logging.WARNING, lambda: f"'{s_level_name_from_config}' not an acceptable log level")
		return i_log_level

	@classmethod
	def get_configuration(cls) -> tuple[int, int, int, int, str, str, str]:
		""""""
		sect_logging: configparser.SectionProxy = CR().get_section_or_default("logging")

		s_level_name_main_logger: str = sect_logging.get(option="level_main_logger", fallback=cls.default_log_level_name_main)
		i_log_level: int = cls.try_translate_level_name_to_level_number(s_level_name_main_logger, cls.default_log_level_main)

		s_level_name_uvicorn_logger: str = sect_logging.get(option="level_uvicorn_logger", fallback=cls.default_log_level_name_uvicorn)
		i_log_level_uvicorn: int = cls.try_translate_level_name_to_level_number(s_level_name_uvicorn_logger, cls.default_log_level_uvicorn)

		s_level_name_file_handler: str = sect_logging.get(option="level_file_handler", fallback=cls.default_log_level_file_handler_name)
		i_log_level_file_handler: int = cls.try_translate_level_name_to_level_number(s_level_name_file_handler, cls.default_log_level_file_handler)

		s_level_name_stream_handler: str = sect_logging.get(option="level_stream_handler", fallback=cls.default_log_level_stream_handler_name)
		i_log_level_stream_handler: int = cls.try_translate_level_name_to_level_number(s_level_name_stream_handler, cls.default_log_level_stream_handler)

		s_file_name: str = sect_logging.get(option="filename", fallback=cls.default_log_file)
		s_encoding: str = sect_logging.get(option="encoding", fallback=cls.default_encoding)
		s_rollover_when: str = sect_logging.get(option="rollover_when", fallback=cls.default_rollover)

		return i_log_level, i_log_level_uvicorn, i_log_level_file_handler, i_log_level_stream_handler, s_file_name, s_encoding, s_rollover_when

	@classmethod
	def set_logging_level_by_number(cls, level: int) -> None:
		""""""
		if level != cls.get_logging_level():
			cls.__new__(cls).logger.setLevel(level)

	@classmethod
	def set_logging_level_by_name(cls, s_level: str) -> None:
		"""
		The program has received a URL call to change the log level.
		"""
		# If name wasn't valid, we wouldn't have gotten this far.
		s_level = s_level.upper()
		i_log_level: int = LoggingHelper.get_level_from_name(s_level)
		if i_log_level != cls.get_logging_level():
			cls.instance.logger.setLevel(i_log_level)
			for handler in cls.instance.logger.handlers:
				handler.setLevel(i_log_level)
			cls.uvicorn_access_logger.setLevel(i_log_level)
			cls.uvicorn_error_logger.setLevel(i_log_level)

	@classmethod
	def get_logging_level(cls) -> int:
		return cls.__new__(cls).logger.level

	@classmethod
	def get_logging_level_name(cls) -> str:
		""""""
		return logging.getLevelName(cls.get_logging_level())

	# Present clean methods for logging
	@classmethod
	def log(cls, i_log_level: int, message: typing.Callable[[], str]) -> None:
		""""""
		if cls.get_logging_level() <= i_log_level:
			cls.__new__(cls).logger.log(i_log_level, message())

	@classmethod
	def log_exception(cls, s_message: str, exception: Exception) -> None:
		cls.instance.logger.exception(s_message, exc_info=exception)
