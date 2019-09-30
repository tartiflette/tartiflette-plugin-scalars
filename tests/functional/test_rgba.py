import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_rgba_ok():
    @Resolver("Query.rgba", schema_name="test_rgba_ok")
    async def rgba_resolver(*_args, **_kwargs):
        return "rgba(51, 170, 51, .1)"

    sdl = """
    type Query {
        rgba: RGBA
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_rgba_ok",
    )

    assert await engine.execute("query rgbaOk { rgba }") == {
        "data": {"rgba": "rgba(51, 170, 51, .1)"}
    }


@pytest.mark.asyncio
async def test_rgba_nok():
    @Resolver("Query.rgba", schema_name="test_rgba_nok")
    async def rgba_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        rgba: RGBA
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_rgba_nok",
    )

    result = await engine.execute("query rgbaNok { rgba }")
    assert result["data"]["rgba"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"] == "Value is not a valid RGBA: < nope >"
    )
