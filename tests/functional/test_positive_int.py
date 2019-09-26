import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_positive_int_ok():
    @Resolver("Query.positiveInt", schema_name="test_positive_int_ok")
    async def positive_int_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        positiveInt: PositiveInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_int_ok",
    )

    assert await engine.execute("query positiveIntOk { positiveInt }") == {
        "data": {"positiveInt": 999}
    }


@pytest.mark.asyncio
async def test_positive_int_nok():
    @Resolver("Query.positiveInt", schema_name="test_positive_int_nok")
    async def positive_int_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        positiveInt: PositiveInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_int_nok",
    )

    result = await engine.execute("query positiveIntNok { positiveInt }")
    assert result["data"]["positiveInt"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "invalid literal for int() with base 10: 'nope'"
    )
