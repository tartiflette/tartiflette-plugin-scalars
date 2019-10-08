import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.rgba import RGBA


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1234, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("abcdef", ValueError, None),
        ("rgba(51, 170, 51, .1)", None, "rgba(51, 170, 51, .1)"),
        ("rgba(51, 170, 51,  1)", None, "rgba(51, 170, 51,  1)"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = RGBA()
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
        (
            StringValueNode(value="rgba(51, 170, 51, .1)"),
            "rgba(51, 170, 51, .1)",
        ),
        (
            StringValueNode(value="rgba(51, 170, 51,  1)"),
            "rgba(51, 170, 51,  1)",
        ),
    ],
)
def test_parse_literal(input_val, output_val):
    assert RGBA().parse_literal(input_val) == output_val
