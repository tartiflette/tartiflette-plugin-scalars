import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.rgb import RGB


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1234, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("abcdef", ValueError, None),
        ("rgb(255,0,153)", None, "rgb(255,0,153)"),
        ("rgb(100%, 0%, 60%)", None, "rgb(100%, 0%, 60%)"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = RGB()
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
        (StringValueNode(value="rgb(255,0,153)"), "rgb(255,0,153)"),
        (StringValueNode(value="rgb(100%, 0%, 60%)"), "rgb(100%, 0%, 60%)"),
    ],
)
def test_parse_literal(input_val, output_val):
    assert RGB().parse_literal(input_val) == output_val
