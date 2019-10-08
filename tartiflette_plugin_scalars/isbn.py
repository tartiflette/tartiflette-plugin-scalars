import re

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

_ISBN_REGEXES = [
    re.compile(
        r"""^(?:ISBN(?:-10)?:? *((?=\d{1,5}([ -]?)\d{1,7}\2?\d{1,6}\2?\d)(?:\d\2*){9}[\dX]))$"""
    ),
    re.compile(
        r"""^(?:ISBN(?:-13)?:? *(97(?:8|9)([ -]?)(?=\d{1,5}\2?\d{1,7}\2?\d{1,6}\2?\d)(?:\d\2*){9}\d))$"""
    ),
]


def _check_isbn(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(
            f"ISBN cannot represent a non string value: < {value} >"
        )
    match = False
    if value != "":
        for isbn_regex in _ISBN_REGEXES:
            if isbn_regex.search(value):
                match = True
                break
    if not match:
        raise ValueError(f"Value is not a valid ISBN: < {value} >")
    return value


class ISBN:
    """
    Scalar which handles International Standard Book Numbers (10/13)
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[str, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's an ISBN, UNDEFINED_VALUE otherwise
        :rtype: Union[str, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _check_isbn(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> str:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's an ISBN
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't an ISBN
        """
        return _check_isbn(value)

    @staticmethod
    def coerce_output(value: str) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's an ISBN
        :rtype: str
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't an ISBN
        """
        return _check_isbn(value)
