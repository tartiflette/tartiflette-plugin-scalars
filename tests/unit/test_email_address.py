import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.email_address import (
    EmailAddress,
    _check_email_address,
)


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("dailymotion.com", ValueError, None),
        ("alice.girardguittard@dm.com", None, "alice.girardguittard@dm.com"),
        ("maxime@dm.com", None, "maxime@dm.com"),
        ("tribe-scale@dm.com", None, "tribe-scale@dm.com"),
        ("alice.girard+guittard@dm.com", None, "alice.girard+guittard@dm.com"),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = EmailAddress()
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
            StringValueNode(value="alice.girardguittard@dm.com"),
            "alice.girardguittard@dm.com",
        ),
        (
            StringValueNode(value="alice.girard-guittard@dm.com"),
            "alice.girard-guittard@dm.com",
        ),
    ],
)
def test_parse_literal_email_address(input_val, output_val):
    assert EmailAddress().parse_literal(input_val) == output_val
