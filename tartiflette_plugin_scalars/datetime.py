from datetime import datetime
from typing import Union

from dateutil.parser import isoparse
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _get_datetime(value: str) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return isoparse(value)
    raise TypeError(f"DateTime cannot represent values other than strings: < {value} >")


def _parse_date(value: str) -> datetime:
    try:
        # get datetime, mirror behavior of NaiveDateTime
        value = _get_datetime(value)
    # reraise any exceptions from parse_naive_date
    except Exception as e:
        raise e
    else:
        if value.tzinfo is None:
            raise ValueError(f"DateTime cannot be timezone naive: < {value} >")
        else:
            return value


class DateTime:
    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[datetime, "UNDEFINED_VALUE"]:
        """
        gets input from AST node
        :param ast: Node to coerce
        :type ast: ValueNode
        :return: the value as a non-naive datetime object
        :rtype: Union[datetime, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _parse_date(ast.value)
            except (ValueError, TypeError, OverflowError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int]) -> datetime:
        """
        Gets a non-naive datetime from input value
        :param value:
        :type value: Union[str, int]
        :return: the value as a non naive datetime
        :raises TypeError: if the value isn't a string or int
        :raises ValueError: if the value isn't convertible to a datetime or is tz naive
        :rtype: datetime
        """
        return _parse_date(value)

    @staticmethod
    def coerce_output(value: datetime) -> str:
        """
        Gets JSON ready output value.
        :param value: the value to coerce
        :type value: datetime
        :return: the string value of the datetime
        :raises: TypeError: if not a datetime
        :rtype: str
        """
        if isinstance(value, datetime):
            return value.isoformat()
        raise TypeError(f"DateTime cannot represent value: < {value} >")
