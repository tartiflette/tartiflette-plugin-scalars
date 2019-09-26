import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_non_positive_int_ok():
    @Resolver("Query.nonPositiveInt", schema_name="test_non_positive_int_ok")
    async def non_positive_int_resolver(*_args, **_kwargs):
        return -999

    sdl = """
    type Query {
        nonPositiveInt: NegativeInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_positive_int_ok",
    )

    assert await engine.execute(
        "query nonPositiveIntOk { nonPositiveInt }"
    ) == {"data": {"nonPositiveInt": -999}}


@pytest.mark.asyncio
async def test_non_positive_int_nok():
    @Resolver("Query.nonPositiveInt", schema_name="test_non_positive_int_nok")
    async def non_positive_int_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        nonPositiveInt: NegativeInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_positive_int_nok",
    )

    result = await engine.execute("query nonPositiveIntNok { nonPositiveInt }")
    assert result["data"]["nonPositiveInt"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "invalid literal for int() with base 10: 'nope'"
    )
