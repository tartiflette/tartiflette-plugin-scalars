from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)


def _parse_non_positive_float(value: Union[str, int, float]) -> float:
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        value = float(value)
    if not isinstance(value, float):
        raise TypeError(
            f"NonPositiveFloat cannot represent values other than strings and numbers: < {value} >"
        )
    if value > 0:
        raise ValueError(
            f"NonPositiveFloat cannot represent values above 0: < {value} >"
        )
    return value


class NonPositiveFloat:
    """
    Scalar which handles non positive floating point numbers
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[float, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's can be parsed as a non positive floating point number, UNDEFINED_VALUE otherwise
        :rtype: Union[float, UNDEFINED_VALUE]
        """
        if isinstance(ast, (FloatValueNode, StringValueNode, IntValueNode)):
            try:
                return _parse_non_positive_float(ast.value)
            except (TypeError, ValueError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int, float]) -> float:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's a non positive float
        :rtype: float
        :raises TypeError: if the value isn't parseable as a float
        :raises ValueError: if the value is positive
        """
        return _parse_non_positive_float(value)

    @staticmethod
    def coerce_output(value: Union[str, int, float]) -> float:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: Any
        :return: the value if it's a non positive float
        :rtype: float
        :raises TypeError: if the value isn't parseable as a float
        :raises ValueError: if the value is positive
        """
        return _parse_non_positive_float(value)
