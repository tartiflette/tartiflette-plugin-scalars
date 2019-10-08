from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _parse_us_currency(value: str) -> int:
    if isinstance(value, str):
        return float(value[1:]) * 100
    raise TypeError(
        f"USCurrency cannot represent values other than strings: < {value} >"
    )


class USCurrency:
    """
    Scalar which handles USD amounts (in format $XX.YY)
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[int, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value in cents if it can be parsed, UNDEFINED_VALUE otherwise
        :rtype: Union[int, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _parse_us_currency(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> int:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value in cents if it can be parsed
        :rtype: int
        :raises TypeError: if the value isn't a string or int
        :raises ValueError: if the value isn't convertible to an int
        """
        return _parse_us_currency(value)

    @staticmethod
    def coerce_output(value: int) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: int
        :return: the value as a USD string if it can be parsed
        :raises TypeError: if the value isn't an int
        :rtype: str
        """
        if isinstance(value, int):
            return "$" + "{0:.2f}".format(value / 100.00)
        raise TypeError(f"USCurrency cannot represent value: < {value} >")
