import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.json import JSON


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("ok", ValueError, None),
        ('"ok"', None, "ok"),
        ("true", None, True),
        ('{"key": "value"}', None, {"key": "value"}),
        ("[1, 2, 3]", None, [1, 2, 3]),
        ("1", None, 1),
        ("null", None, None),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = JSON()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val",
    [
        (False, "false"),
        ("ok", '"ok"'),
        ({"key": "value"}, '{"key": "value"}'),
        ([1, 2, 3], "[1, 2, 3]"),
        (1, "1"),
        (None, "null"),
    ],
)
def test_coerce_output(input_val, output_val):
    scalar = JSON()
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
        (StringValueNode(value='"ok"'), "ok"),
        (StringValueNode(value="true"), True),
    ],
)
def test_parse_literal(input_val, output_val):
    assert JSON().parse_literal(input_val) == output_val
