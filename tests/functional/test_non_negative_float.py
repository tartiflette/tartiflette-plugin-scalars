import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_negative_float_ok():
    @Resolver(
        "Query.nonNegativeFloat", schema_name="test_non_negative_float_ok"
    )
    async def negative_float_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        nonNegativeFloat: NonNegativeFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_negative_float_ok",
    )

    assert await engine.execute(
        "query nonNegativeFloatOk { nonNegativeFloat }"
    ) == {"data": {"nonNegativeFloat": 999}}


@pytest.mark.asyncio
async def test_negative_float_nok():
    @Resolver(
        "Query.nonNegativeFloat", schema_name="test_non_negative_float_nok"
    )
    async def negative_float_resolver(*_args, **_kwargs):
        return -999

    sdl = """
    type Query {
        nonNegativeFloat: NonNegativeFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_negative_float_nok",
    )

    result = await engine.execute(
        "query nonNegativeFloatNok { nonNegativeFloat }"
    )
    assert result["data"]["nonNegativeFloat"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "NonNegativeFloat cannot represent values below 0: < -999.0 >"
    )
