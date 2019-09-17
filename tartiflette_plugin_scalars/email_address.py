import re

from typing import Any, Union

from tartiflette.constants import UNDEFINED_VALUE

EMAIL_ADDRESS_REGEX = re.compile(
    r"""^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"""
)


def check_email_address(value: Any):
    if not isinstance(value, str):
        raise TypeError(
            f"EmailAddress cannot represent a non string value: < {value} >"
        )
    if not EMAIL_ADDRESS_REGEX.search(value):
        raise ValueError(f"Value is not a valid email address: < {value} >")
    return value


class EmailAddress:
    def parse_literal(self, ast: "ValueNode") -> Union[Any, type(UNDEFINED_VALUE)]:
        if isinstance(ast, StringValueNode) and EMAIL_ADDRESS_REGEX.search(
            ast.value
        ):
            return ast.value
        return UNDEFINED_VALUE

    def coerce_input(self, value: Any) -> str:
        return check_email_address(value)

    def coerce_output(self, value: Any) -> Any:
        return check_email_address(value)
