import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.port import Port


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        (-100, ValueError, None),
        (0, ValueError, None),
        (65535, None, 65535),
        (120, None, 120),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = Port()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
        with pytest.raises(exception):
            scalar.coerce_output(input_val)
    else:
        assert scalar.coerce_output(input_val) == output_val
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
        (IntValueNode(value=0), UNDEFINED_VALUE),
        (IntValueNode(value=80), 80),
        (IntValueNode(value=65535), 65535),
    ],
)
def test_parse_literal(input_val, output_val):
    assert Port().parse_literal(input_val) == output_val
