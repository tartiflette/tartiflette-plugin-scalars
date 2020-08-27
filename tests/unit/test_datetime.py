import datetime

import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    IntValueNode,
    StringValueNode,
)

from dateutil.tz import tzutc
from tartiflette_plugin_scalars.datetime import DateTime


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        (2 ** 128, TypeError, None),
        ("dailymotion", ValueError, None),
        (
            "2019-09-20T14:30:28+00:00",
            None,
            datetime.datetime(2019, 9, 20, 14, 30, 28, tzinfo=tzutc()),
        ),
        ("2019-09-20T14:30:28", ValueError, None),
        (1568988000, TypeError, None),
        (datetime.datetime(2019, 9, 9, 16, 0, 0), ValueError, None),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = DateTime()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val",
    [
        (
            datetime.datetime(2019, 9, 9, 16, 0, 0, tzinfo=tzutc()),
            "2019-09-09T16:00:00+00:00",
        ),
        (
            datetime.datetime(2018, 8, 16, tzinfo=tzutc()),
            "2018-08-16T00:00:00+00:00",
        ),
        ("2018-08-16T00:00:00+00:00", "2018-08-16T00:00:00+00:00")
    ],
)
def test_coerce_output(input_val, output_val):
    scalar = DateTime()
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
        (IntValueNode(value=2 ** 128), UNDEFINED_VALUE),
        (
            StringValueNode(value="2019-09-20T14:30:28+00:00"),
            datetime.datetime(2019, 9, 20, 14, 30, 28, tzinfo=tzutc()),
        ),
        (StringValueNode(value="2019-09-20T14:30:28"), UNDEFINED_VALUE),
        (IntValueNode(value=1568988000), UNDEFINED_VALUE),
    ],
)
def test_parse_literal(input_val, output_val):
    assert DateTime().parse_literal(input_val) == output_val
