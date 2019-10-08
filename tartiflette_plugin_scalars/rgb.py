import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_RGB_REGEX = re.compile(
    r"""^rgb\(\s*(-?\d+|-?\d*\.\d+(?=%))(%?)\s*,\s*(-?\d+|-?\d*\.\d+(?=%))(\2)\s*,\s*(-?\d+|-?\d*\.\d+(?=%))(\2)\s*\)$"""
)


def _check_rgb(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"RGB cannot represent a non string value: < {value} >"
        )
    if not _RGB_REGEX.search(value):
        raise ValueError(f"Value is not a valid RGB: < {value} >")
    return value


class RGB:
    """
    Scalar which handles the Red, Green, Blue representation of a color
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a RGB, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_rgb(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a RGB
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a RGB
        """
        return _check_rgb(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Loads the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a RGB
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a RGB
        """
        return _check_rgb(value)
