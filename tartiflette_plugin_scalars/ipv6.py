from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _parse_ipv6(value: str) -> IPv6Address:
    if isinstance(value, str):
        value = ip_address(value)
    if isinstance(value, IPv6Address):
        return value
    if isinstance(value, IPv4Address):
        raise ValueError("IPv6 cannot be used to represent IPv4 addresses")
    raise TypeError(
        f"IPv6 cannot represent values other than strings and IPv6Address: < {value} >"
    )


class IPv6:
    """
    Scalar which handles Internet Protocol version 6 addresses
    """

    @staticmethod
    def parse_literal(
        ast: "ValueNode",
    ) -> Union[IPv6Address, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value as a IPv6Address object if it can be parsed, UNDEFINED_VALUE otherwise
        :rtype: Union[IPv6Address, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _parse_ipv6(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> IPv6Address:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value as a IPv6Address object if it can be parsed
        :rtype: IPv6Address
        :raises TypeError: if the value isn't a string or int
        :raises ValueError: if the value isn't convertible to a IPv6Address
        """
        return _parse_ipv6(value)

    @staticmethod
    def coerce_output(value: IPv6Address) -> str:
        """
        Loads the output value
        :param value: the value to coerce
        :type value: IPv6Address
        :return: the value as a IPv6Address object if it can be parsed
        :raises TypeError: if the value isn't a IPv6Address
        :rtype: str
        """
        if isinstance(value, IPv6Address):
            return str(value)
        raise TypeError(f"IPv6 cannot represent value: < {value} >")
