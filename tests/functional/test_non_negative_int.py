import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_negative_int_ok():
    @Resolver("Query.nonNegativeInt", schema_name="test_non_negative_int_ok")
    async def negative_int_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        nonNegativeInt: NonNegativeInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_negative_int_ok",
    )

    assert await engine.execute(
        "query nonNegativeIntOk { nonNegativeInt }"
    ) == {"data": {"nonNegativeInt": 999}}


@pytest.mark.asyncio
async def test_negative_int_nok():
    @Resolver("Query.nonNegativeInt", schema_name="test_non_negative_int_nok")
    async def negative_int_resolver(*_args, **_kwargs):
        return -999

    sdl = """
    type Query {
        nonNegativeInt: NonNegativeInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_negative_int_nok",
    )

    result = await engine.execute("query nonNegativeIntNok { nonNegativeInt }")
    assert result["data"]["nonNegativeInt"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "NonNegativeInt cannot represent values below 0: < -999 >"
    )
