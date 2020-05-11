from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Union  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _parse_ipv4(value: str) -> IPv4Address:
    if isinstance(value, str):
        value = ip_address(value)
    if isinstance(value, IPv4Address):
        return value
    if isinstance(value, IPv6Address):
        raise ValueError("IPv4 cannot be used to represent IPv6 addresses")
    raise TypeError(
        f"IPv4Address cannot represent values other than strings and IPv4Address: < {value} >"
    )


class IPv4:
    """
    Scalar which handles Internet Protocol version 4 addresses
    """

    @staticmethod
    def parse_literal(
        ast: "ValueNode",
    ) -> Union[IPv4Address, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value as a IPv4Address object if it can be parsed, UNDEFINED_VALUE otherwise
        :rtype: Union[IPv4Address, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _parse_ipv4(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> IPv4Address:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value as a IPv4Address object if it can be parsed
        :rtype: IPv4Address
        :raises TypeError: if the value isn't a string or int
        :raises ValueError: if the value isn't convertible to a IPv4Address
        """
        return _parse_ipv4(value)

    @staticmethod
    def coerce_output(value: IPv4Address) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: IPv4Address
        :return: the value as a IPv4Address object if it can be parsed
        :raises TypeError: if the value isn't a IPv4Address
        :rtype: str
        """
        if isinstance(value, IPv4Address):
            return str(value)
        raise TypeError(f"IPv4 cannot represent value: < {value} >")
