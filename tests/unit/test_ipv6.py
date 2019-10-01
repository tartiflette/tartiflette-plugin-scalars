import ipaddress

import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.ipv6 import IPv6


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("dailymotion", ValueError, None),
        ("127.0.0.1", ValueError, None),
        (
            "2001:0db8:0000:0000:0000:8a2e:0370:7334",
            None,
            ipaddress.ip_address("2001:0db8:0000:0000:0000:8a2e:0370:7334"),
        ),
        ("::1", None, ipaddress.ip_address("::1")),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = IPv6()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val",
    [
        (
            ipaddress.ip_address("2001:0db8:0000:0000:0000:8a2e:0370:7334"),
            "2001:db8::8a2e:370:7334",
        ),
        (ipaddress.ip_address("::1"), "::1"),
    ],
)
def test_coerce_output(input_val, output_val):
    scalar = IPv6()
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
        (StringValueNode(value="::1"), ipaddress.ip_address("::1")),
    ],
)
def test_parse_literal(input_val, output_val):
    assert IPv6().parse_literal(input_val) == output_val
