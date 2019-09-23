import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_negative_float_ok():
    @Resolver("Query.negativeFloat", schema_name="test_negative_float_ok")
    async def negative_float_resolver(*_args, **_kwargs):
        return -999.99

    sdl = """
    type Query {
        negativeFloat: NegativeFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_negative_float_ok",
    )

    assert await engine.execute("query negativeFloatOk { negativeFloat }") == {
        "data": {"negativeFloat": -999.99}
    }


@pytest.mark.asyncio
async def test_negative_float_nok():
    @Resolver("Query.negativeFloat", schema_name="test_negative_float_nok")
    async def negative_float_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        negativeFloat: NegativeFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_negative_float_nok",
    )

    result = await engine.execute("query negativeFloatNok { negativeFloat }")
    assert result["data"]["negativeFloat"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "could not convert string to float: 'nope'"
    )
