import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    FloatValueNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.positive_float import PositiveFloat


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("nok", ValueError, None),
        ("-12.3", ValueError, -12.3),
        (-12.3, ValueError, -12.3),
        (-1, ValueError, -1.0),
        (0, ValueError, None),
        ("1", None, 1.0),
        (2, None, 2.0),
        (3.5, None, 3.5),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = PositiveFloat()
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
        (FloatValueNode(value=-16.5), UNDEFINED_VALUE),
        (IntValueNode(value=0), UNDEFINED_VALUE),
        (StringValueNode(value="12.3"), 12.3),
        (IntValueNode(value=15), 15),
        (FloatValueNode(value=16.5), 16.5),
    ],
)
def test_parse_literal(input_val, output_val):
    assert PositiveFloat().parse_literal(input_val) == output_val
