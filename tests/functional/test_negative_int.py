import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_negative_int_ok():
    @Resolver("Query.negativeInt", schema_name="test_negative_int_ok")
    async def negative_int_resolver(*_args, **_kwargs):
        return -999

    sdl = """
    type Query {
        negativeInt: NegativeInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_negative_int_ok",
    )

    assert await engine.execute("query negativeIntOk { negativeInt }") == {
        "data": {"negativeInt": -999}
    }


@pytest.mark.asyncio
async def test_negative_int_nok():
    @Resolver("Query.negativeInt", schema_name="test_negative_int_nok")
    async def negative_int_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        negativeInt: NegativeInt
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_negative_int_nok",
    )

    result = await engine.execute("query negativeIntNok { negativeInt }")
    assert result["data"]["negativeInt"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "invalid literal for int() with base 10: 'nope'"
    )


@pytest.mark.asyncio
async def test_negative_int_nok_mutation_ok():
    @Resolver(
        "Mutation.negativeInt", schema_name="test_negative_int_mutation_ok"
    )
    async def negative_int_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        negativeInt: NegativeInt
    }

    type Mutation {
        negativeInt(input: NegativeInt): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_negative_int_mutation_ok",
    )

    assert await engine.execute(
        "mutation negativeInt { negativeInt(input:-100) }"
    ) == {"data": {"negativeInt": True}}


@pytest.mark.asyncio
async def test_negative_int_mutation_nok():
    @Resolver(
        "Mutation.negativeInt", schema_name="test_negative_int_mutation_nok"
    )
    async def negativeInt_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        negativeInt: NegativeInt
    }

    type Mutation {
        negativeInt(input: NegativeInt): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_negative_int_mutation_nok",
    )

    result = await engine.execute(
        "mutation negativeInt { negativeInt(input:100) }"
    )
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value 100 is not of correct type NegativeInt"
    )
