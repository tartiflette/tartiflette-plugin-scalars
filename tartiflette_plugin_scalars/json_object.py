import json

from typing import Any  # pylint: disable=unused-import

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _parse_json_object(value: str) -> Any:
    if isinstance(value, str):
        try:
            result = json.loads(value)
        except json.decoder.JSONDecodeError as err:
            raise ValueError(
                f"Value is not a valid JSON value: < {value} >"
            ) from err
        if isinstance(result, dict):
            return result
        raise ValueError(f"Value is not a valid JSON object: < {value} >")
    raise TypeError(
        f"JSON cannot represent values other than strings: < {value} >"
    )


class JSONObject:
    """
    Scalar which handles JSON objects
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> dict:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value parsed from JSON if it's an object, UNDEFINED_VALUE otherwise
        :rtype: dict
        """
        if isinstance(ast, StringValueNode):
            try:
                return _parse_json_object(ast.value)
            except (ValueError, TypeError):
                return UNDEFINED_VALUE
        return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> dict:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value parsed from JSON if it's an object
        :rtype: dict
        :raises TypeError: if the value isn't a string
        """
        return _parse_json_object(value)

    @staticmethod
    def coerce_output(value: dict) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: Any
        :return: the value dumped to JSON
        :rtype: str
        :raises TypeError: if the value isn't a dict
        """
        if isinstance(value, dict):
            return json.dumps(value)
        raise TypeError(f"JSONObject cannot represent value: < {value} >")
