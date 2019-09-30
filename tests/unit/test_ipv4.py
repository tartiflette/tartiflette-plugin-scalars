import ipaddress

import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.ipv4 import IPv4


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("dailymotion", ValueError, None),
        ("2001:0db8:0000:0000:0000:8a2e:0370:7334", ValueError, None),
        ("127.0.0.1", None, ipaddress.ip_address("127.0.0.1")),
        ("8.8.8.8", None, ipaddress.ip_address("8.8.8.8")),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = IPv4()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val",
    [
        (ipaddress.ip_address("127.0.0.1"), "127.0.0.1"),
        (ipaddress.ip_address("8.8.8.8"), "8.8.8.8"),
    ],
)
def test_coerce_output(input_val, output_val):
    scalar = IPv4()
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
            StringValueNode(value="127.0.0.1"),
            ipaddress.ip_address("127.0.0.1"),
        ),
    ],
)
def test_parse_literal(input_val, output_val):
    assert IPv4().parse_literal(input_val) == output_val
