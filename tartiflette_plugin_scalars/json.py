import json

from typing import Any  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _parse_json(value: str) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError as err:
            raise ValueError(
                f"Value is not a valid JSON value: < {value} >"
            ) from err
    raise TypeError(
        f"JSON cannot represent values other than strings: < {value} >"
    )


class JSON:
    """
    Scalar which handles JSON values
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Any:
        """
        Dumps the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value parsed from JSON, UNDEFINED_VALUE otherwise
        :rtype: Any
        """
        if isinstance(ast, StringValueNode):
            try:
                return _parse_json(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> Any:
        """
        Dumps the input value
        :param value: the value to coerce
        :type value: str
        :return: the value parsed from JSON
        :rtype: int
        :raises TypeError: if the value isn't a string
        """
        return _parse_json(value)

    @staticmethod
    def coerce_output(value: Any) -> str:
        """
        Loads the output value
        :param value: the value to coerce
        :type value: Any
        :return: the value dumped to JSON
        :rtype: str
        """
        return json.dumps(value)
