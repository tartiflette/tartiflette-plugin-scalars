import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_unsigned_int_ok():
    @Resolver("Query.unsignedInt", schema_name="test_unsigned_int_ok")
    async def unsigned_int_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        unsignedInt: UnsignedInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_unsigned_int_ok",
    )

    assert await engine.execute("query unsignedIntOk { unsignedInt }") == {
        "data": {"unsignedInt": 999}
    }


@pytest.mark.asyncio
async def test_unsigned_int_nok():
    @Resolver("Query.unsignedInt", schema_name="test_unsigned_int_nok")
    async def unsigned_int_resolver(*_args, **_kwargs):
        return -2

    sdl = """
    type Query {
        unsignedInt: UnsignedInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_unsigned_int_nok",
    )

    result = await engine.execute("query unsignedIntNok { unsignedInt }")
    assert result["data"]["unsignedInt"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "UnsignedInt cannot represent values below 0: < -2 >"
    )
