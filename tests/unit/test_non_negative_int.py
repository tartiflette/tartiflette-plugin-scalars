import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.non_negative_int import NonNegativeInt


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("nok", ValueError, None),
        ("-1", ValueError, None),
        (-2, ValueError, None),
        (-3.5, ValueError, None),
        ("12", None, 12),
        (12, None, 12),
        (1.5, None, 1),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = NonNegativeInt()
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
        (StringValueNode(value="-12.3"), UNDEFINED_VALUE),
        (IntValueNode(value=-15), UNDEFINED_VALUE),
        (IntValueNode(value=0), 0),
        (FloatValueNode(value=16.0), 16),
        (IntValueNode(value=15), 15),
        (StringValueNode(value="15"), 15),
    ],
)
def test_parse_literal(input_val, output_val):
    assert NonNegativeInt().parse_literal(input_val) == output_val
