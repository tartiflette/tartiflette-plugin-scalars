import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_EMAIL_ADDRESS_REGEX = re.compile(
    r"""^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
)


def _check_email_address(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"EmailAddress cannot represent a non string value: < {value} >"
        )
    if not _EMAIL_ADDRESS_REGEX.search(value):
        raise ValueError(f"Value is not a valid email address: < {value} >")
    return value


class EmailAddress:
    """
    Scalar which handles email addresses
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's an email, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_email_address(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's an email
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't an email
        """
        return _check_email_address(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's an email
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't an email
        """
        return _check_email_address(value)
