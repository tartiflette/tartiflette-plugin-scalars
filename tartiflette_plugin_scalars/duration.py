from datetime import timedelta
from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _parse_duration(value: str) -> timedelta:
    def get_kv(_arg: str) -> dict:
        try:
            _key, _value = _arg.split("=")
        except ValueError:
            raise ValueError(
                f"Duration argument has more or less than 2 elements: < {_arg} >"
            )
        else:
            if _key in VALID_KEYS:
                try:
                    return {_key: int(_value)}
                except ValueError:
                    raise ValueError(
                        f"Duration argument value is not an int: < {_arg} >"
                    )
            else:
                raise ValueError(f"Duration argument has invalid key: < {_arg} >")

    VALID_KEYS = (
        "days",
        "seconds",
        "microseconds",
        "milliseconds",
        "minutes",
        "hours",
        "weeks",
    )
    # make a timedelta from a comma separated string
    # remove whitespace and split by comma
    arg_list = value.replace(" ", "").split(",")
    arg_dict = {}
    for arg in arg_list:
        if "=" in arg:
            arg_dict.update(get_kv(arg))
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
    def coerce_input(value: Union[str, int]) -> timedelta:
        return _parse_duration(value)

    @staticmethod
    def coerce_output(value: timedelta) -> str:
        return str(value)
