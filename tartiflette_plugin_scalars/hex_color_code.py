import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_HEX_COLOR_CODE_REGEX = re.compile(
    r"""^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{8})$"""
)


def _check_hex_color_code(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"HexColorCode cannot represent a non string value: < {value} >"
        )
    if not _HEX_COLOR_CODE_REGEX.search(value):
        raise ValueError(f"Value is not a valid HexColorCode: < {value} >")
    return value


class HexColorCode:
    """
    Scalar which handles hexadecimal color codes
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a HexColorCode, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_hex_color_code(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a HexColorCode
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a HexColorCode
        """
        return _check_hex_color_code(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a HexColorCode
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a HexColorCode
        """
        return _check_hex_color_code(value)
