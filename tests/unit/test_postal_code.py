import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.postal_code import PostalCode


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("nok", ValueError, None),
        ("75017", None, "75017"),
        ("K1N 9N1", None, "K1N 9N1"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = PostalCode()
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
        (StringValueNode(value="75017"), "75017"),
        (StringValueNode(value="K1N 9N1"), "K1N 9N1"),
    ],
)
def test_parse_literal_email_address(input_val, output_val):
    assert PostalCode().parse_literal(input_val) == output_val
