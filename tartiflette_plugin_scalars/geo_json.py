import json

from typing import Any

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode

import geojson


def _parse_json(value: str) -> Any:
    if isinstance(value, str):
        try:
            return geojson.loads(value)
        except json.decoder.JSONDecodeError as err:
            raise ValueError(
                f"Value is not a valid GeoJSON value: < {value} >"
            ) from err
    raise TypeError(
        f"GeoJSON cannot represent values other than strings: < {value} >"
    )


class GeoJSON:
    """
    Scalar which handles GeoJSON values
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Any:
        """
        Dumps the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value parsed from GeoJSON, UNDEFINED_VALUE otherwise
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
        :return: the value parsed from GeoJSON
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
        :return: the value dumped to GeoJSON
        :rtype: str
        """
        try:
            return geojson.dumps(value, sort_keys=True)
        except TypeError as err:
            raise ValueError(
                f"Object of type {type(value).__name__} is not GeoJSON serializable"
            ) from err
