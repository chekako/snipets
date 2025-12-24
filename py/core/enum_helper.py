# Standard Library
from enum import Enum


# TODO: TODO: Make sure this still works.
class EnumHelper:
	""""""
	# To avoid repeating the part where we collect all values in an Enum
	dict_enums_and_members: dict[str, set[str]] = dict()

	@classmethod
	def is_value_in_enum(cls, cls_enum: type[Enum], value: str) -> bool:
		""""""
		s_class_name: str = cls_enum.__name__
		set_values: set[str] | None = cls.dict_enums_and_members.get(s_class_name)
		if set_values is None:
			# lst_values: list[str] = [item.value for item in cls_enum]
			# set_values: set[str] = set(lst_values)
			# cls.dict_enums_and_members[s_class_name] = set_values
			cls.dict_enums_and_members[s_class_name] = {item.value for item in cls_enum}
		return value in set_values
