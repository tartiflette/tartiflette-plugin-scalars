from urllib.parse import ParseResult

import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.url import URL


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("dailymtion", ValueError, None),
        (
            "https://www.dailymotion.com/play",
            None,
            ParseResult(
                scheme="https",
                netloc="www.dailymotion.com",
                path="/play",
                params="",
                query="",
                fragment="",
            ),
        ),
        (
            ParseResult(
                scheme="https",
                netloc="www.dailymotion.com",
                path="/play",
                params="",
                query="",
                fragment="",
            ),
            None,
            ParseResult(
                scheme="https",
                netloc="www.dailymotion.com",
                path="/play",
                params="",
                query="",
                fragment="",
            ),
        ),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = URL()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (
            ParseResult(
                scheme="https",
                netloc="www.dailymotion.com",
                path="/play",
                params="",
                query="",
                fragment="",
            ),
            None,
            "https://www.dailymotion.com/play",
        ),
        (
            ParseResult(
                scheme="", netloc="", path="", params="", query="", fragment=""
            ),
            ValueError,
            None,
        ),
    ],
)
def test_coerce_output(input_val, exception, output_val):
    scalar = URL()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_output(input_val)
    else:
        assert scalar.coerce_output(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val",
    [
        (
            DirectiveDefinitionNode(
                arguments=[], name="directive", locations=None
            ),
            UNDEFINED_VALUE,
        ),
        (StringValueNode(value="nok"), UNDEFINED_VALUE),
        (
            StringValueNode(value="https://www.dailymotion.com/play"),
            ParseResult(
                scheme="https",
                netloc="www.dailymotion.com",
                path="/play",
                params="",
                query="",
                fragment="",
            ),
        ),
    ],
)
def test_parse_literal_email_address(input_val, output_val):
    assert URL().parse_literal(input_val) == output_val
