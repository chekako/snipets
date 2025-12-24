# Standard Library
import datetime
import logging
import typing


# TODO: Consider color-coding some messages by log level (WARNING=yellow, ERROR/CRITICAL=red)
class CustomFormatter(logging.Formatter):
	"""
	Define a custom formatter for log files. Take the time and format it in UTC, to one micro-second.
	"""

	def __init__(self, fmt, datefmt):  # style='%',
		super().__init__(fmt, datefmt, validate=True)
		self.default_date_format = "%Y-%m-%dT%H:%M:%S.%f"

	#     def format(self, record):
	#         # Customize the log record here
	#         record.message = record.message.upper()  # Example: Convert message to uppercase
	#         return super().format(record)

	# %F = %Y-%m-%d
	# %T = %H:%M:%S

	@typing.override
	def formatTime(self, record: logging.LogRecord, datefmt: str | None = '%Y-%m-%dT%H:%M:%S.%f') -> str:
		""""""
		dt: datetime.datetime = datetime.datetime.fromtimestamp(record.created)
		if datefmt:
			return f"{dt.strftime(datefmt)}"
		return f"{dt.isoformat()}"
