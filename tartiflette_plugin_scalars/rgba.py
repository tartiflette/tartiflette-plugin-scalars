import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_RGBA_REGEX = re.compile(
    r"""^rgba\(\s*(-?\d+|-?\d*\.\d+(?=%))(%?)\s*,\s*(-?\d+|-?\d*\.\d+(?=%))(\2)\s*,\s*(-?\d+|-?\d*\.\d+(?=%))(\2)\s*,\s*(-?\d+|-?\d*.\d+)\s*\)$"""
)


def _check_rgba(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"RGBA cannot represent a non string value: < {value} >"
        )
    if not _RGBA_REGEX.search(value):
        raise ValueError(f"Value is not a valid RGBA: < {value} >")
    return value


class RGBA:
    """
    Scalar which handles the Red, Green, Blue and Alpha representation of a color
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a RGBA, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_rgba(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a RGBA
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a RGBA
        """
        return _check_rgba(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a RGBA
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a RGBA
        """
        return _check_rgba(value)
