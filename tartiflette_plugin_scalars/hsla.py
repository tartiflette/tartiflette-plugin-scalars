import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_HSLA_REGEX = re.compile(
    r"""^hsla\(\s*(-?\d+|-?\d*.\d+)(turn|rad|deg|)\s*,\s*(-?\d+|-?\d*.\d+)%\s*,\s*(-?\d+|-?\d*.\d+)%\s*,\s*(-?\d+|-?\d*.\d+)\s*\)$"""
)


def _check_hsla(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"HSLA cannot represent a non string value: < {value} >"
        )
    if not _HSLA_REGEX.search(value):
        raise ValueError(f"Value is not a valid HSLA: < {value} >")
    return value


class HSLA:
    """
    Scalar which handles the Hue, Saturation, Lightness and Alpha representation of a color
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Dumps the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a HSLA, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_hsla(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Dumps the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a HSLA
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a HSLA
        """
        return _check_hsla(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Loads the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a HSLA
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a HSLA
        """
        return _check_hsla(value)
