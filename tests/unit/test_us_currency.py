import datetime

import pytest

from dateutil.tz import tzutc
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    IntValueNode,
    StringValueNode,
)

from tartiflette_plugin_scalars.us_currency import USCurrency


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("50€", ValueError, None),
        ("$50.00", None, 5000),
        ("$0.00", None, 0),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = USCurrency()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val", [(5000, "$50.00"), (0, "$0.00")]
)
def test_coerce_output(input_val, output_val):
    scalar = USCurrency()
    assert scalar.coerce_output(input_val) == output_val


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
        (IntValueNode(value=10), UNDEFINED_VALUE),
        (StringValueNode(value="$50.00"), 5000),
    ],
)
def test_parse_literal(input_val, output_val):
    assert USCurrency().parse_literal(input_val) == output_val
