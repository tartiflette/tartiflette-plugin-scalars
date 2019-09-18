import pytest

from tartiflette_plugin_scalars import bake


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "schema_name,config,sdl",
    [
        ("empty_conf", {}, "scalar EmailAddress"),
        ("disable_all", {"email_address": {"enabled": False}}, ""),
        (
            "enable_all",
            {"email_address": {"enabled": True}},
            "scalar EmailAddress",
        ),
        (
            "rename_all",
            {"email_address": {"name": "MyEmailAddress"}},
            "scalar MyEmailAddress",
        ),
    ],
)
async def test_bake(schema_name, config, sdl):
    assert (await bake(schema_name, config)) == sdl
