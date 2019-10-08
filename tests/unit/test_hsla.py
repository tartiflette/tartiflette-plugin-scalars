import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.hsla import HSLA


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1234, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("abcdef", ValueError, None),
        ("hsla(270, 60%, 50%, .05)", None, "hsla(270, 60%, 50%, .05)"),
        (
            "hsla(4.71239rad, 60%, 70%, 1)",
            None,
            "hsla(4.71239rad, 60%, 70%, 1)",
        ),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = HSLA()
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
            StringValueNode(value="hsla(270, 60%, 50%, .05)"),
            "hsla(270, 60%, 50%, .05)",
        ),
        (
            StringValueNode(value="hsla(4.71239rad, 60%, 70%, 1)"),
            "hsla(4.71239rad, 60%, 70%, 1)",
        ),
    ],
)
def test_parse_literal(input_val, output_val):
    assert HSLA().parse_literal(input_val) == output_val
