from datetime import datetime
from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

from dateutil.parser import isoparse


def _get_datetime(value: str) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return isoparse(value)
    raise TypeError(
        f"DateTime cannot represent values other than strings: < {value} >"
    )


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
    def coerce_input(value: str) -> datetime:
        """
        Gets a non-naive datetime from input value
        :param value:
        :type value: str
        :return: the value as a non naive datetime
        :raises TypeError: if the value isn't a string
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
        if isinstance(value, str):
            try:
                return isoparse(value).isoformat()
            except ValueError as err:
                raise ValueError(
                    f"DateTime cannot represent value: < {value} >"
                ) from err
        raise TypeError(f"DateTime cannot represent value: < {value} >")
