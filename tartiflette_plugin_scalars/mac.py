import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_MAC_REGEX = re.compile(
    r"""^(?:[0-9A-Fa-f]{2}([:-]?)[0-9A-Fa-f]{2})(?:(?:\1|\.)(?:[0-9A-Fa-f]{2}([:-]?)[0-9A-Fa-f]{2})){2}$"""
)


def _check_mac(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"MAC cannot represent a non string value: < {value} >"
        )
    if not _MAC_REGEX.search(value):
        raise ValueError(f"Value is not a valid MAC address: < {value} >")
    return value


class MAC:
    """
    Scalar which handles Media Access Control addresses
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a MAC address, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_mac(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a MAC address
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a mac address
        """
        return _check_mac(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a MAC address
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a mac address
        """
        return _check_mac(value)
