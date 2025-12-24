# Standard Library
import time
import typing
# MY Code (must avoid circular imports)
import core


class AutoLog:
	""""""
	i_id: int = 0
	start_key_outer: str = "\u2554"  # ╔
	start_key_inner: str = "\u231C"  # ⌜
	end_key_outer: str = "\u255D"  # ╝
	end_key_inner: str = "\u231F"  # ⌟

	def __init__(self, log_level: int, s_common_name: str,
	             enter_msg: typing.Callable | None = lambda: "",
	             exit_msg: typing.Callable | None = lambda: "") -> None:
		self.id = f"-{AutoLog.i_id}"
		AutoLog.i_id += 1
		self.common = s_common_name
		self.log_level = log_level
		self.enter_msg: typing.Callable = enter_msg
		self.exit_msg: typing.Callable = exit_msg

	def __del__(self):
		pass

	def __enter__(self) -> 'AutoLog':
		self.ts = time.time()
		# Redundant, but maybe slower without it
		# if main_logger.get_logging_level() <= self.log_level:
		core.L.MainLogger().log(self.log_level, lambda: f"{self.id} {AutoLog.start_key_outer} {self.common} {AutoLog.start_key_inner} {self.enter_msg()}")
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		# Redundant, but maybe slower without it
		# if main_logger.get_logging_level() <= self.log_level:
		core.L.MainLogger().log(self.log_level, lambda: f"{self.id} {AutoLog.end_key_outer} {self.common} {AutoLog.end_key_inner} {self.exit_msg()} in {time.time() - self.ts} s")
