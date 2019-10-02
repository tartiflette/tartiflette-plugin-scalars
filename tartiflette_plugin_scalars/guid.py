import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_GUID_REGEX = re.compile(
    r"""[0-9a-f]{8}-?[0-9a-f]{4}-?[1-5][0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$"""
)


def _check_guid(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"GUID cannot represent a non string value: < {value} >"
        )
    if not _GUID_REGEX.search(value):
        raise ValueError(f"Value is not a valid GUID: < {value} >")
    return value


class GUID:
    """
    Scalar which handles Globally Unique Identifiers
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a GUID, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_guid(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a GUID
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a GUID
        """
        return _check_guid(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a GUID
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a GUID
        """
        return _check_guid(value)
