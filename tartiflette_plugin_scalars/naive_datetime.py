from datetime import datetime
from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import IntValueNode, StringValueNode

from dateutil.parser import isoparse


def _parse_naive(value: Union[int, str]) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return datetime.utcfromtimestamp(value)
    if isinstance(value, str):
        return isoparse(value)
    raise TypeError(
        f"NaiveDateTime cannot represent values other than strings and ints: < {value} >"
    )


class NaiveDateTime:
    """
    Scalar which handles date and time objects
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[datetime, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value as a datetime object if it can be parsed, UNDEFINED_VALUE otherwise
        :rtype: Union[datetime, UNDEFINED_VALUE]
        """
        if isinstance(ast, (IntValueNode, StringValueNode)):
            try:
                return _parse_naive(ast.value)
            except (ValueError, TypeError, OverflowError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int]) -> datetime:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: Union[str, int]
        :return: the value as a datetime object if it can be parsed
        :rtype: datetime
        :raises TypeError: if the value isn't a string or int
        :raises ValueError: if the value isn't convertible to a datetime
        :raises OverflowError: if the value is an int too large to be a unix timestamp
        """
        return _parse_naive(value)

    @staticmethod
    def coerce_output(value: datetime) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: datetime
        :return: the value as a datetime object if it can be parsed
        :raises TypeError: if the value isn't a datetime
        :rtype: str
        """
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, str):
            try:
                datetime.fromisoformat(value)
            except ValueError as err:
                raise ValueError(
                    f"NaiveDateTime cannot represent value: < {value} >"
                ) from err
            else:
                return value
        raise TypeError(f"NaiveDateTime cannot represent value: < {value} >")
