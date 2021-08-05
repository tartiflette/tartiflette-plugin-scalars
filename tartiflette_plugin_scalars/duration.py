from datetime import timedelta
from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_VALID_KEYS = (
    "days",
    "seconds",
    "microseconds",
    "milliseconds",
    "minutes",
    "hours",
    "weeks",
)


def _get_kv(arg: str) -> dict:

    try:
        key, value = arg.split("=")
    except ValueError as err:
        raise ValueError(
            f"Duration argument has more or less than 2 elements: < {arg} >"
        ) from err
    else:
        if key in _VALID_KEYS:
            try:
                return {key: int(value)}
            except ValueError as err:
                raise ValueError(
                    f"Duration argument value is not an int: < {arg} >"
                ) from err
        else:
            raise ValueError(f"Duration argument has invalid key: < {arg} >")


def _parse_duration(value: str) -> timedelta:
    if not isinstance(value, str):
        raise TypeError(f"<{value}> is not a string!")

    # make a timedelta from a comma separated string
    # remove whitespace and split by comma
    arg_list = value.replace(" ", "").split(",")
    arg_dict = {}
    for arg in arg_list:
        if "=" in arg:
            arg_dict.update(_get_kv(arg))
        else:
            raise ValueError(f"Duration key missing '=': < {value} >")
    return timedelta(**arg_dict)


class Duration:
    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[timedelta, "UNDEFINED_VALUE"]:
        if isinstance(ast, StringValueNode):
            try:
                return _parse_duration(ast.value)
            except (ValueError, TypeError, OverflowError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> timedelta:
        return _parse_duration(value)

    @staticmethod
    def coerce_output(value: timedelta) -> str:
        if isinstance(value, timedelta):
            return value.__str__()
        raise TypeError(f"Duration cannot represent value: < {value} >")
