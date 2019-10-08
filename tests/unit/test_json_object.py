import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.json_object import JSONObject


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("ok", ValueError, None),
        ('"ok"', ValueError, None),
        ("true", ValueError, None),
        ("[1, 2, 3]", ValueError, None),
        ("1", ValueError, None),
        ("null", ValueError, None),
        ('{"key": "value"}', None, {"key": "value"}),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = JSONObject()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, "false"),
        ("ok", TypeError, '"ok"'),
        ([1, 2, 3], TypeError, "[1, 2, 3]"),
        (1, TypeError, "1"),
        (None, TypeError, "null"),
        ({"key": "value"}, None, '{"key": "value"}'),
    ],
)
def test_coerce_output(input_val, exception, output_val):
    scalar = JSONObject()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_output(input_val)
    else:
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
        (StringValueNode(value='"ok"'), UNDEFINED_VALUE),
        (StringValueNode(value="true"), UNDEFINED_VALUE),
        (StringValueNode(value='{"key": "value"}'), {"key": "value"}),
    ],
)
def test_parse_literal(input_val, output_val):
    assert JSONObject().parse_literal(input_val) == output_val
