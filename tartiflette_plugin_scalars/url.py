from typing import Union  # pylint: disable=unused-import
from urllib.parse import ParseResult, urlparse, urlunparse

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _parse_url(value: Union[str, ParseResult]) -> ParseResult:
    if isinstance(value, str):
        try:
            value = urlparse(value)
        except AttributeError as err:
            raise TypeError(
                f"URL cannot represent values other than strings and ParseResult: < {value} >"
            ) from err
    if isinstance(value, ParseResult):
        if value.netloc:
            return value
        raise ValueError(f"Value is not a valid URL: < {value} >")
    raise TypeError(
        f"URL cannot represent values other than strings and ParseResult: < {value} >"
    )


class URL:
    """
    Scalar which handles URL objects
    """

    @staticmethod
    def parse_literal(
        ast: "ValueNode",
    ) -> Union[ParseResult, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value as a ParseResult tuple if it can be parsed, UNDEFINED_VALUE otherwise
        :rtype: Union[ParseResult, UNDEFINED_VALUE]
        """
        if isinstance(ast, StringValueNode):
            try:
                return _parse_url(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: Union[str, ParseResult]) -> ParseResult:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value as a ParseResult tuple if it can be parsed
        :rtype: ParseResult
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a URL
        """
        return _parse_url(value)

    @staticmethod
    def coerce_output(value: ParseResult) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: ParseResult
        :return: the value as string
        :rtype: str
        """
        if isinstance(value, ParseResult) and value.netloc:
            return urlunparse(value)
        raise ValueError(f"URL cannot represent value: < {value} >")
