# Standard Library
import logging


class LoggingHelper:
	""""""
	dict_name_to_level = logging.getLevelNamesMapping()

	@staticmethod
	def get_level_name(i_level: int) -> str:
		# I have a numeric level. I need a string name.
		return logging.getLevelName(i_level)

	@staticmethod
	def get_level_from_name(s_name: str) -> int | None:
		# I have a string name. I need a numeric level.
		return LoggingHelper.dict_name_to_level.get(s_name)
