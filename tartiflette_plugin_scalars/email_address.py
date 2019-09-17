import re

from typing import Any, Union

from tartiflette.constants import UNDEFINED_VALUE

EMAIL_ADDRESS_REGEX = re.compile(
    r"""/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/"""
)


class EmailAddress:
    def _is_email_address(self, value: Any):
        if not isinstance(value, str):
            raise TypeError(
                f"EmailAddress cannot represent a non string value: < {value} >"
            )
        if EMAIL_ADDRESS_REGEX.search(value):
            raise ValueError(f"Value is not string: < {value} >")
        return value

    def parse_literal(self, ast: "ValueNode") -> Union[Any, UNDEFINED_VALUE]:
        if isinstance(ast, StringValueNode) and EMAIL_ADDRESS_REGEX.search(
            ast.value
        ):
            return ast.value
        return UNDEFINED_VALUE

    def coerce_input(self, value: Any) -> str:
        return self._is_email_address(value)

    def coerce_output(self, value: Any) -> Any:
        return self._is_email_address(value)
