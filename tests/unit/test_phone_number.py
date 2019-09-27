import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.phone_number import PhoneNumber


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("abcdef", ValueError, None),
        ("+33177351100", None, "+33177351100"),
        ("+16502530001", None, "+16502530001"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = PhoneNumber()
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
        (StringValueNode(value="+33177351100"), "+33177351100"),
        (StringValueNode(value="+16502530001"), "+16502530001"),
    ],
)
def test_parse_literal_email_address(input_val, output_val):
    assert PhoneNumber().parse_literal(input_val) == output_val
