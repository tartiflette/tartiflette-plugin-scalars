import pytest

from tartiflette_plugin_scalars import _generate_scalars


@pytest.mark.parametrize(
    "schema_name,config,scalars",
    [
        ("empty_conf", {}, ["scalar EmailAddress", "scalar DateTime"]),
        (
            "disable_all",
            {
                "email_address": {"enabled": False},
                "datetime": {"enabled": False},
            },
            [],
        ),
        (
            "enable_all",
            {
                "email_address": {"enabled": True},
                "datetime": {"enabled": True},
            },
            ["scalar EmailAddress", "scalar DateTime"],
        ),
        (
            "rename_all",
            {
                "email_address": {"name": "MyEmailAddress"},
                "datetime": {"name": "MyDateTime"},
            },
            ["scalar MyEmailAddress", "scalar MyDateTime"],
        ),
    ],
)
def test_generate_scalars(schema_name, config, scalars):
    assert sorted(_generate_scalars(schema_name, config)) == sorted(scalars)
