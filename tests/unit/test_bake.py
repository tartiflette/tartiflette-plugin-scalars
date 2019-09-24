import pytest

from tartiflette_plugin_scalars import _generate_scalars


@pytest.mark.parametrize(
    "schema_name,config,scalars",
    [
        (
            "empty_conf",
            {},
            [
                "scalar EmailAddress",
                "scalar DateTime",
                "scalar NegativeFloat",
                "scalar NegativeInt",
                "scalar NonNegativeFloat",
                "scalar NonNegativeInt",
            ],
        ),
        (
            "disable_all",
            {
                "email_address": {"enabled": False},
                "datetime": {"enabled": False},
                "negative_float": {"enabled": False},
                "negative_int": {"enabled": False},
                "non_negative_float": {"enabled": False},
                "non_negative_int": {"enabled": False},
            },
            [],
        ),
        (
            "enable_all",
            {
                "email_address": {"enabled": True},
                "datetime": {"enabled": True},
                "negative_float": {"enabled": True},
                "negative_int": {"enabled": True},
                "non_negative_float": {"enabled": True},
                "non_negative_int": {"enabled": True},
            },
            [
                "scalar EmailAddress",
                "scalar DateTime",
                "scalar NegativeFloat",
                "scalar NegativeInt",
                "scalar NonNegativeFloat",
                "scalar NonNegativeInt",
            ],
        ),
        (
            "rename_all",
            {
                "email_address": {"name": "MyEmailAddress"},
                "datetime": {"name": "MyDateTime"},
                "negative_float": {"name": "MyNegativeFloat"},
                "negative_int": {"name": "MyNegativeInt"},
                "non_negative_float": {"name": "MyNonNegativeFloat"},
                "non_negative_int": {"name": "MyNonNegativeInt"},
            },
            [
                "scalar MyEmailAddress",
                "scalar MyDateTime",
                "scalar MyNegativeFloat",
                "scalar MyNegativeInt",
                "scalar MyNonNegativeFloat",
                "scalar MyNonNegativeInt",
            ],
        ),
    ],
)
def test_generate_scalars(schema_name, config, scalars):
    assert sorted(_generate_scalars(schema_name, config)) == sorted(scalars)
