import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_rgb_ok():
    @Resolver("Query.rgb", schema_name="test_rgb_ok")
    async def rgb_resolver(*_args, **_kwargs):
        return "rgb(100%, 0%, 60%)"

    sdl = """
    type Query {
        rgb: RGB
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_rgb_ok",
    )

    assert await engine.execute("query rgbOk { rgb }") == {
        "data": {"rgb": "rgb(100%, 0%, 60%)"}
    }


@pytest.mark.asyncio
async def test_rgb_nok():
    @Resolver("Query.rgb", schema_name="test_rgb_nok")
    async def rgb_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        rgb: RGB
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_rgb_nok",
    )

    result = await engine.execute("query rgbNok { rgb }")
    assert result["data"]["rgb"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"] == "Value is not a valid RGB: < nope >"
    )
