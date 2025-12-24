# MY Code
import core


def try_parse_int(val: str, fallback: int) -> int:
	"""
	NOTES (in no particular order):
	1) If "val" is a string representation of a float, this will still work.
	"""
	try:
		return int(val)
	except ValueError as val_err:
		core.L.MainLogger().log(core.L.WARNING, lambda: f"error parsing int...{", ".join(val_err.args)}\nDefaulting to {fallback}")
		return fallback


def try_parse_float(val: str, fallback: float) -> float:
	"""
	NOTES (in no particular order):
	1) If "val" is a string representation of an integer, this will still work.
	"""
	try:
		return float(val)
	except ValueError as val_err:
		s_message: str = f"error parsing float...{", ".join(val_err.args)}\nDefaulting to {fallback}"
		core.L.MainLogger().log(core.L.WARNING, lambda: s_message)
		return fallback


def try_parse_boolean(val: str, fallback: bool) -> bool:
	"""
	Try to get a proper Python boolean value from a string.

	NOTES (in no particular order):
	1) Permit string representations of "true" and "false, accounting for any case or mix of cases,
	such as "TRUE", "True", "true", "tRuE", or some other mix.
	"""
	if val.lower() == "true":
		return True
	elif val.lower() == "false":
		return False
	else:
		core.L.MainLogger().log(core.L.WARNING, lambda: f"Error parsing boolean '{val}'\nDefaulting to {fallback}")
		return fallback


def try_parse_int_check_against_min(val: str, val_id: str, i_min: int, i_fallback: int) -> int:
	"""
	Handle repeated process of trying to parse an integer from a string, comparing it to a minimum
	value, and logging a warning if it's less than the minimum.
	"""
	i_val: int = try_parse_int(val, i_fallback)
	if i_val < i_min:
		i_val = i_fallback
		core.L.MainLogger().log(core.L.WARNING, lambda: f"{val_id} must be at least {i_min}")
	return i_val


def try_parse_float_check_against_min(val: str, val_id: str, fl_min: float, fl_fallback: float) -> float:
	"""
	Handle repeated process of trying to parse a float from a string, comparing it to a minimum
	value, and logging a warning if it's less than the minimum.
	"""
	fl_val: float = try_parse_float(val, fl_fallback)
	if fl_val < fl_min:
		fl_val = fl_fallback
		core.L.MainLogger().log(core.L.WARNING, lambda: f"{val_id} must be at least {fl_min}")
	return fl_val
