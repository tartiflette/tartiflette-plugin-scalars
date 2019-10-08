import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_HSL_REGEX = re.compile(
    r"""^hsl\(\s*(-?\d+|-?\d*.\d+)(turn|rad|deg|)\s*,\s*(-?\d+|-?\d*.\d+)%\s*,\s*(-?\d+|-?\d*.\d+)%\s*\)$"""
)


def _check_hsl(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"HSL cannot represent a non string value: < {value} >"
        )
    if not _HSL_REGEX.search(value):
        raise ValueError(f"Value is not a valid HSL: < {value} >")
    return value


class HSL:
    """
    Scalar which handles the Hue, Saturation and Lightness representation of a color
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a HSL, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_hsl(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a HSL
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a HSL
        """
        return _check_hsl(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a HSL
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a HSL
        """
        return _check_hsl(value)
