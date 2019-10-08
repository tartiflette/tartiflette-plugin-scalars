from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)

_MAX_UNSIGNED_INT = 4294967296  # 2^32
_MIN_UNSIGNED_INT = 0


def _parse_unsigned_int(value):  # lgtm [py/similar-function]
    if isinstance(value, (str, float)):
        value = int(value)
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(
            f"UnsignedInt cannot represent values other than strings and numbers: < {value} >"
        )
    if value >= _MAX_UNSIGNED_INT:
        raise ValueError(
            f"UnsignedInt cannot represent values above or equal to 2^32: < {value} >"
        )
    if value < _MIN_UNSIGNED_INT:
        raise ValueError(
            f"UnsignedInt cannot represent values below 0: < {value} >"
        )
    return value


class UnsignedInt:
    """
    Scalar which handles integers between 0 (included) and 2^32 (excluded)
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[int, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it can be parsed as an unsigned int, UNDEFINED_VALUE otherwise
        :rtype: Union[int, UNDEFINED_VALUE]
        """
        if isinstance(ast, (FloatValueNode, StringValueNode, IntValueNode)):
            try:
                return _parse_unsigned_int(ast.value)
            except (TypeError, ValueError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int, float]) -> int:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's an unsigned int
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't contained in the [0, 2^32[ range
        """
        return _parse_unsigned_int(value)

    @staticmethod
    def coerce_output(value: Union[str, int, float]) -> int:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's an int
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't contained in the [0, 2^32[ range
        """
        return _parse_unsigned_int(value)
