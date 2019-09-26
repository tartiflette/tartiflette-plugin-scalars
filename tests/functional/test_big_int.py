import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_big_int_ok():
    @Resolver("Query.bigInt", schema_name="test_big_int_ok")
    async def big_int_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        bigInt: Long
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_big_int_ok",
    )

    assert await engine.execute("query bigIntOk { bigInt }") == {
        "data": {"bigInt": 999}
    }


@pytest.mark.asyncio
async def test_big_int_nok():
    @Resolver("Query.bigInt", schema_name="test_big_int_nok")
    async def big_int_resolver(*_args, **_kwargs):
        return 2 ** 64

    sdl = """
    type Query {
        bigInt: Long
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_big_int_nok",
    )

    result = await engine.execute("query bigIntNok { bigInt }")
    assert result["data"]["bigInt"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Long cannot represent values above or equal to 2^63: < 18446744073709551616 >"
    )
