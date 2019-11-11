# PYTHON
from datetime import timedelta

# 3RD PARTY
import pytest

# TARTIFLETTE
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import (
    DirectiveDefinitionNode,
    StringValueNode,
    IntValueNode,
    BooleanValueNode,
)
from tartiflette_plugin_scalars.duration import Duration


# parse literal
@pytest.mark.parametrize(
    "input_value,output_value",
    [
        (BooleanValueNode(value=True), UNDEFINED_VALUE),
        (IntValueNode(value=12345), UNDEFINED_VALUE),
        (
            DirectiveDefinitionNode(arguments=[], name="directive", locations=[]),
            UNDEFINED_VALUE,
        ),
        (StringValueNode(value="days=1, seconds=20"), timedelta(days=1, seconds=20)),
        (StringValueNode(value="bad_value"), UNDEFINED_VALUE),
    ],
)
def test_parse_literal(input_value, output_value):
    assert Duration().parse_literal(input_value) == output_value


# coerce input
@pytest.mark.parametrize(
    "input_value,exception,output_value",
    [
        # BAD VALUES
        (False, TypeError, None),
        ("", ValueError, None),
        ("testtesttest", ValueError, None),
        ("days=bad_value", ValueError, None),
        ("bad_key=1", ValueError, None),
        ("days=1 seconds=string", ValueError, None),
        (1.2345, TypeError, None),
        (123456, TypeError, None),
        # GOOD VALUES
        ("days=1, seconds=2", None, timedelta(days=1, seconds=2)),
        ("hours=1, weeks=2", None, timedelta(weeks=2, hours=1)),
    ],
)
def test_coerce_input(input_value, exception, output_value):
    scalar = Duration()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_value)
    else:
        assert scalar.coerce_input(input_value) == output_value


# coerce output
@pytest.mark.parametrize(
    "input_value,output_value",
    [
        (timedelta(seconds=5, microseconds=399774), "0:00:05.399774"),
        (timedelta(weeks=2, hours=3), "14 days, 3:00:00"),
        (timedelta(weeks=50, hours=20, seconds=20), "350 days, 20:00:20"),
    ],
)
def test_coerce_output(input_value, output_value):
    assert Duration().coerce_output(input_value) == output_value
