# Standard Library
import datetime
from typing import TypeVar


NullableNumber = TypeVar('NullableNumber', int, None)  # Must be exactly int or None
NullableString = TypeVar("NullableString", str, None)  # Must be exactly str or None
NullableBoolean = TypeVar("NullableBoolean", bool, None)
NullableNumberString = TypeVar("NullableNumberString", int, str, None)
NullableNumberStringDate = TypeVar("NullableNumberStringDate", int, str, datetime.date, None)
