import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_long_ok():
    @Resolver("Query.long", schema_name="test_long_ok")
    async def long_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        long: Long
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_long_ok",
    )

    assert await engine.execute("query longOk { long }") == {
        "data": {"long": 999}
    }


@pytest.mark.asyncio
async def test_long_nok():
    @Resolver("Query.long", schema_name="test_long_nok")
    async def long_resolver(*_args, **_kwargs):
        return 2 ** 64

    sdl = """
    type Query {
        long: Long
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_long_nok",
    )

    result = await engine.execute("query longNok { long }")
    assert result["data"]["long"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Long cannot represent values above or equal to 2^63: < 18446744073709551616 >"
    )
