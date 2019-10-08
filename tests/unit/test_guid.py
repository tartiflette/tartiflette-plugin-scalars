import pytest

from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.guid import GUID


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (1234, TypeError, None),
        (False, TypeError, None),
        ("", ValueError, None),
        ("abcdef", ValueError, None),
        (
            "5591b4e9-c747-45ae-8abf-d9cd1a17081e",
            None,
            "5591b4e9-c747-45ae-8abf-d9cd1a17081e",
        ),
        (
            "74af0909-3a1a-4c6b-b3d3-6e76c10348e5",
            None,
            "74af0909-3a1a-4c6b-b3d3-6e76c10348e5",
        ),
    ],
)
def test_coerce_input_output(input_val, exception, output_val):
    scalar = GUID()
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
            StringValueNode(value="5591b4e9-c747-45ae-8abf-d9cd1a17081e"),
            "5591b4e9-c747-45ae-8abf-d9cd1a17081e",
        ),
        (
            StringValueNode(value="74af0909-3a1a-4c6b-b3d3-6e76c10348e5"),
            "74af0909-3a1a-4c6b-b3d3-6e76c10348e5",
        ),
    ],
)
def test_parse_literal(input_val, output_val):
    assert GUID().parse_literal(input_val) == output_val
