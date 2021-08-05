import uuid

from typing import Union

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode


def _create_uuid(value: str) -> uuid.UUID:
    if not isinstance(value, str):
        raise TypeError(
            f"UUID cannot represent a non string value: < {value} >"
        )
    try:
        return uuid.UUID(value)
    except ValueError as err:
        raise ValueError(f"Value is not a valid UUID: < {value} >") from err


class UUID:
    """
    Scalar which handles UUID.
    """

    @staticmethod
    def parse_literal(ast: "ValueNode") -> Union[uuid.UUID, "UNDEFINED_VALUE"]:
        """
        Loads the input value from an AST node
        :param ast: ast node to coerce
        :type ast: ValueNode
        :return: the value if it's a UUID, UNDEFINED_VALUE otherwise
        :rtype: Union[uuid.UUID, UNDEFINED_VALUE]
        """
        if not isinstance(ast, StringValueNode):
            return UNDEFINED_VALUE
        try:
            return _create_uuid(ast.value)
        except (ValueError, TypeError):
            return UNDEFINED_VALUE

    @staticmethod
    def coerce_input(value: str) -> uuid.UUID:
        """
        Loads the input value
        :param value: the value to coerce
        :type value: str
        :return: the value if it's a UUID
        :rtype: uuid.UUID
        :raises TypeError: if the value isn't a string
        :raises ValueError: if the value isn't a UUID
        """
        return _create_uuid(value)

    @staticmethod
    def coerce_output(value: uuid.UUID) -> str:
        """
        Dumps the output value
        :param value: the value to coerce
        :type value: str
        :return: the uuid as string
        :rtype: str
        :raises TypeError: if the value isn't a string
        """
        if not isinstance(value, uuid.UUID):
            raise TypeError(f"Value is not instance of UUID: < {value} >")
        return str(value)
