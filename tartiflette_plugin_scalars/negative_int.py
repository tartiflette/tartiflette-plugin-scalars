from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)


def _parse_negative_int(value: Union[str, int, float]) -> int:
    if isinstance(value, (str, float)):
        value = int(value)
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(
            f"NegativeInt cannot represent values other than strings and numbers: < {value} >"
        )
    if value >= 0:
        raise ValueError(
            f"NegativeInt cannot represent values above 0: < {value} >"
        )
    return value


class NegativeInt:
    """
    Scalar which handles negative integers
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[int, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it can be parsed as a negative integer, UNDEFINED_VALUE otherwise
        :rtype: Union[int, UNDEFINED_VALUE]
        """
        if isinstance(ast, (FloatValueNode, StringValueNode, IntValueNode)):
            try:
                return _parse_negative_int(ast.value)
            except (TypeError, ValueError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int, float]) -> int:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's a negative int
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't negative
        """
        return _parse_negative_int(value)

    @staticmethod
    def coerce_output(value: Union[str, int, float]) -> int:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's a negative int
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't negative
        """
        return _parse_negative_int(value)
