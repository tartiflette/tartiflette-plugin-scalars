import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_PHONE_NUMBER_REGEX = re.compile(r"""^\+\d{11,15}$""")


def _check_phone_number(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"PhoneNumber cannot represent a non string value: < {value} >"
        )
    if not _PHONE_NUMBER_REGEX.search(value):
        raise ValueError(f"Value is not a valid phone number: < {value} >")
    return value


class PhoneNumber:
    """
    Scalar which handles phone numbers conforming to the E.164 format
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a phone number, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_phone_number(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a phone number
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a phone number
        """
        return _check_phone_number(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a phone number
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a phone number
        """
        return _check_phone_number(value)
