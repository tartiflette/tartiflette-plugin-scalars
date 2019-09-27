import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.hsl import HSL


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1234, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("abcdef", ValueError, None),
        ("hsl(270, 60%, 50%)", None, "hsl(270, 60%, 50%)"),
        ("hsl(4.71239rad, 60%, 70%)", None, "hsl(4.71239rad, 60%, 70%)"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = HSL()
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
        (StringValueNode(value="hsl(270, 60%, 50%)"), "hsl(270, 60%, 50%)"),
        (
            StringValueNode(value="hsl(4.71239rad, 60%, 70%)"),
            "hsl(4.71239rad, 60%, 70%)",
        ),
    ],
)
def test_parse_literal(input_val, output_val):
    assert HSL().parse_literal(input_val) == output_val
