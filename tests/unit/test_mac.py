import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.mac import MAC


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("127.0.0.1", ValueError, None),
        ("00:0a:95:9d:68:16", None, "00:0a:95:9d:68:16"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = MAC()
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
        (StringValueNode(value="00:0a:95:9d:68:16"), "00:0a:95:9d:68:16"),
    ],
)
def test_parse_literal(input_val, output_val):
    assert MAC().parse_literal(input_val) == output_val
