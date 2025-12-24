# Standard Library
import time


class TimeHelper:
	I_SECONDS_IN_MINUTE: int = 60
	I_MINUTES_IN_HOUR: int = 60

	@classmethod
	def get_right_now_epoch_seconds(cls) -> int:
		"""
		Get the number of seconds since the Epoch.

		:return: Integer = the number of whole seconds since the Epoch
		"""
		return int(time.time())

	# Convert Time Units
	@classmethod
	def convert_minutes_to_seconds(cls, i_fl_minutes: int | float) -> int:
		""""""
		return int(cls.I_SECONDS_IN_MINUTE * i_fl_minutes)

	@classmethod
	def convert_hours_to_seconds(cls, fl_hours: float) -> int:
		""""""
		return int(cls.I_SECONDS_IN_MINUTE * cls.I_MINUTES_IN_HOUR * fl_hours)
