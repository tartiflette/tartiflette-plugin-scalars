import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.big_int import BigInt


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("nok", ValueError, None),
        (2 ** 100, None, 2 ** 100),
        (-(2 ** 100), None, -(2 ** 100)),
        ("-1", None, -1),
        ("1", None, 1),
        (2, None, 2),
        (3.0, None, 3),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = BigInt()
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
        (IntValueNode(value=2 ** 100), 2 ** 100),
        (IntValueNode(value=-(2 ** 100)), -(2 ** 100)),
        (IntValueNode(value=0), 0),
        (IntValueNode(value=-15), -15),
        (FloatValueNode(value=16.0), 16),
        (StringValueNode(value="12"), 12),
        (IntValueNode(value=15), 15),
    ],
)
def test_parse_literal(input_val, output_val):
    assert BigInt().parse_literal(input_val) == output_val
