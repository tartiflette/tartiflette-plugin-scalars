from datetime import datetime
from typing import Any, Union #pylint: disable=unused-import

from dateutil.parser import isoparse
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import IntValueNode, StringValueNode


def _parse_date(value: Union[int, str]) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return datetime.fromtimestamp(value)
    if isinstance(value, str):
        return isoparse(value)
    raise TypeError(
        f"DateTime cannot represent values other than strings and ints: < {value} >"
    )


class DateTime:
    """
    Scalar which handles date and time objects
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[datetime, "UNDEFINED_VALUE"]:
        """
        Coerce the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value as a datetime object if it can be parsed, UNDEFINED_VALUE otherwise
        :rtype: Union[datetime, UNDEFINED_VALUE]
        """
        if isinstance(ast, (IntValueNode, StringValueNode)):
            try:
                return _parse_date(ast.value)
            except (ValueError, TypeError, OverflowError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int]) -> datetime:
        """
        Coerce the input value
        :param value: the value to coerce
        :type value: Union[str, int]
        :return: the value as a datetime object if it can be parsed
        :raises TypeError: if the value isn't a string or int
        :raises ValueError: if the value isn't convertible to a datetime
        :raises OverflowError: if the value is an int too large to be a unix timestamp
        """
        return _parse_date(value)

    @staticmethod
    def coerce_output(value: datetime) -> str:
        """
        Coerce the output value
        :param value: the value to coerce
        :type value: datetime
        :return: the value as a datetime object if it can be parsed
        """
        if isinstance(value, datetime):
            return value.isoformat()
        raise TypeError(f"DateTime cannot represent value: < {value} >")
