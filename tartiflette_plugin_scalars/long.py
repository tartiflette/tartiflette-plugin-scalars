from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)

_MAX_LONG = 9223372036854775808  # 2^63
_MIN_LONG = -9223372036854775808  # -2^63


def _parse_long(value):  # lgtm [py/similar-function]
    if isinstance(value, (str, float)):
        value = int(value)
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(
            f"long cannot represent values other than strings and numbers: < {value} >"
        )
    if value >= _MAX_LONG:
        raise ValueError(
            f"Long cannot represent values above or equal to 2^63: < {value} >"
        )
    if value < _MIN_LONG:
        raise ValueError(
            f"Long cannot represent values below 2^63 : < {value} >"
        )
    return value


class Long:
    """
    Scalar which handles integers between 2^63 (excluded) and -2^63 (included)
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[int, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it can be parsed as a long, UNDEFINED_VALUE otherwise
        :rtype: Union[int, UNDEFINED_VALUE]
        """
        if isinstance(ast, (FloatValueNode, StringValueNode, IntValueNode)):
            try:
                return _parse_long(ast.value)
            except (TypeError, ValueError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int, float]) -> int:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's a long
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't contained in the [2^63, 2^63[ range
        """
        return _parse_long(value)

    @staticmethod
    def coerce_output(value: Union[str, int, float]) -> int:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's an int
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't contained in the [2^63, 2^63[ range
        """
        return _parse_long(value)
