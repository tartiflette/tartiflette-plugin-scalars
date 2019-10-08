import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.isbn import ISBN


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("nok", ValueError, None),
        ("ISBN 0553078143", None, "ISBN 0553078143"),
        ("ISBN 0-06-059518-3", None, "ISBN 0-06-059518-3"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = ISBN()
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
        (StringValueNode(value="ISBN 0-06-059518-3"), "ISBN 0-06-059518-3"),
        (StringValueNode(value="ISBN 0553078143"), "ISBN 0553078143"),
    ],
)
def test_parse_literal_email_address(input_val, output_val):
    assert ISBN().parse_literal(input_val) == output_val
