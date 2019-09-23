import pytest

from tartiflette_plugin_scalars import _generate_scalars


@pytest.mark.parametrize(
    "schema_name,config,scalars",
    [
        (
            "empty_conf",
            {},
            ["scalar EmailAddress", "scalar DateTime", "scalar NegativeFloat"],
        ),
        (
            "disable_all",
            {
                "email_address": {"enabled": False},
                "datetime": {"enabled": False},
                "negative_float": {"enabled": False},
            },
            [],
        ),
        (
            "enable_all",
            {
                "email_address": {"enabled": True},
                "datetime": {"enabled": True},
                "negative_float": {"enabled": True},
            },
            ["scalar EmailAddress", "scalar DateTime", "scalar NegativeFloat"],
        ),
        (
            "rename_all",
            {
                "email_address": {"name": "MyEmailAddress"},
                "datetime": {"name": "MyDateTime"},
                "negative_float": {"name": "NegativeFloat"},
            },
            [
                "scalar MyEmailAddress",
                "scalar MyDateTime",
                "scalar NegativeFloat",
            ],
        ),
    ],
)
def test_generate_scalars(schema_name, config, scalars):
    assert sorted(_generate_scalars(schema_name, config)) == sorted(scalars)
