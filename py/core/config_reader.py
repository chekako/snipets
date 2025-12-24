# Standard Library
import configparser
import os
# MY Code
from core import my_type_aliases


class ConfigReader:
	"""
	read from configuration files.

	Given the choice between INI and JSON, I settled on INI.
	"""
	#
	instance = None
	filepath = "backend_config.ini"
	# filepath = "backend_config.json"  # This file doesn't exist.

	def __new__(cls):
		""""""
		if cls.instance is None:
			cls.instance = super(ConfigReader, cls).__new__(cls)
			cls.instance.my_config = configparser.ConfigParser()  # Use this object to read + manipulate INI file
			cls.instance.my_config.read(cls.filepath)  # read the INI file
		return cls.instance

	@classmethod
	def check_file(cls) -> my_type_aliases.NullableString:
		""""""
		if not os.path.exists(cls.filepath):
			return f"Config file '{cls.filepath}' does not exist."
		if not cls.instance.my_config.sections():
			return f"Config file '{cls.filepath}' is empty."
		return None

	@classmethod
	def get_section_or_default(cls, section_name: str) -> configparser.SectionProxy:
		"""

		NOTES (in no particular order):
		1) This will break if there's no section in the config file called "s_section_name".
			return cls.instance.my_config[s_section_name] or cls.instance.my_config["DEFAULT"]
		2) This doesn't work because it requires an "option" argument.
			abc = cls.instance.my_config.get(section=s_section_name, fallback="DEFAULT")
		"""
		name: str = section_name if cls.instance.my_config.has_section(section_name) else "DEFAULT"
		return cls.instance.my_config[name]

	@classmethod
	def get_string(cls, section: str, option: str, fallback: my_type_aliases.NullableString) -> str:
		""""""
		return cls.get_section_or_default(section).get(option=option, fallback=fallback)

	@classmethod
	def get_int(cls, section: str, option: str, fallback: int) -> int:
		""""""
		return cls.get_section_or_default(section).getint(option=option, fallback=fallback)

	# TODO: Use it or lose it.
	@classmethod
	def get_float(cls, section: str, option: str, fallback: float) -> float:
		""""""
		return cls.get_section_or_default(section).getfloat(option=option, fallback=fallback)

	@classmethod
	def get_boolean(cls, section: str, option: str, fallback: bool) -> bool:
		""""""
		return cls.get_section_or_default(section).getboolean(option=option, fallback=fallback)
