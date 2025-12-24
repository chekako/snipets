# Standard Library
import datetime


class DateHelper:
	ISO_8601_DATE_FORMAT: str = "%Y-%m-%d"  # {yyyy}-{mm}-{dd}
	DASH_SEPARATOR: str = "-"

	@classmethod
	def convert_iso_8601_string_to_date(cls, s_date: str) -> datetime.date:
		""""""
		d_datetime: datetime.datetime = datetime.datetime.strptime(s_date, cls.ISO_8601_DATE_FORMAT)
		return d_datetime.date()

	@classmethod
	def convert_date_to_iso_8601_string(cls, d_date: datetime.date) -> str:
		"""
		Take a Python "datetime.date" object and convert it into a string, representing a date in
		the ISO-8601 format, like: yyyy-mm-dd

		NOTES (in no particular order):
		1) For consistency of visuals and length, we need to check for single-digit month and day
		numbers; if we find one, we pad it with a prefix 0.

		:param d_date:

		:return:
		"""
		i_year: int = d_date.year
		i_month: int = d_date.month
		i_day: int = d_date.day

		s_year: str = str(i_year)
		s_month: str = f"0{i_month}" if i_month < 10 else str(i_month)
		s_day: str = f"0{i_day}" if i_day < 10 else str(i_day)

		lst_date_parts: list[str] = [s_year, s_month, s_day]
		s_iso_date: str = cls.DASH_SEPARATOR.join(lst_date_parts)
		return s_iso_date

	@classmethod
	def get_today(cls) -> datetime.date:
		""""""
		return datetime.date.today()

	@classmethod
	def get_current_year(cls) -> int:
		""""""
		today: datetime.date = cls.get_today()
		return today.year