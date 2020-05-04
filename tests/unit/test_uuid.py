import uuid

import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.uuid import UUID


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1234, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("abcdef", ValueError, None),
        (
            "2869393a-f101-4bea-9b5b-3262611e5c51",
            None,
            uuid.UUID("2869393a-f101-4bea-9b5b-3262611e5c51"),
        ),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = UUID()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


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
        (StringValueNode(value=None), UNDEFINED_VALUE),
        (
            StringValueNode(value="5591b4e9-c747-45ae-8abf-d9cd1a17081e"),
            uuid.UUID("5591b4e9-c747-45ae-8abf-d9cd1a17081e"),
        ),
        (
            StringValueNode(value="ebc43690-83b4-11ea-a48f-acde48001122"),
            uuid.UUID("ebc43690-83b4-11ea-a48f-acde48001122"),
        ),
    ],
)
def test_parse_literal(input_val, output_val):
    assert UUID().parse_literal(input_val) == output_val
