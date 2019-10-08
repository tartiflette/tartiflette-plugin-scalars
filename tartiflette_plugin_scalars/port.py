from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)

_MAX_PORT = 65535
_MIN_PORT = 0


def _parse_port(value: Union[str, int, float]) -> str:
    if isinstance(value, (str, float)):
        value = int(value)
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(
            f"Port cannot represent values other than strings and numbers: < {value} >"
        )
    if value > _MAX_PORT:
        raise ValueError(
            f"Port cannot represent values above 65535: < {value} >"
        )
    if value <= _MIN_PORT:
        raise ValueError(
            f"Port cannot represent values below or equal to 0: < {value} >"
        )
    return value


class Port:
    """
    Scalar which handles integers usable as TCP/UDP port (in range ]0, 65535[)
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[int, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it can be parsed as a port, UNDEFINED_VALUE otherwise
        :rtype: Union[int, UNDEFINED_VALUE]
        """
        if isinstance(ast, (FloatValueNode, StringValueNode, IntValueNode)):
            try:
                return _parse_port(ast.value)
            except (TypeError, ValueError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, int, float]) -> int:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's a port
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't contained in the ]0, 65535] range
        """
        return _parse_port(value)

    @staticmethod
    def coerce_output(value: Union[str, int, float]) -> int:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: Union[str, int, float]
        :return: the value if it's an int
        :rtype: int
        :raises TypeError: if the value isn't parseable as an int
        :raises ValueError: if the value isn't contained in the ]0, 65535] range
        """
        return _parse_port(value)
