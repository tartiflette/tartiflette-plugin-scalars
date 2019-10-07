import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_positive_float_ok():
    @Resolver("Query.positiveFloat", schema_name="test_positive_float_ok")
    async def positive_float_resolver(*_args, **_kwargs):
        return 999.99

    sdl = """
    type Query {
        positiveFloat: PositiveFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_float_ok",
    )

    assert await engine.execute("query positiveFloatOk { positiveFloat }") == {
        "data": {"positiveFloat": 999.99}
    }


@pytest.mark.asyncio
async def test_positive_float_nok():
    @Resolver("Query.positiveFloat", schema_name="test_positive_float_nok")
    async def positive_float_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        positiveFloat: PositiveFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_float_nok",
    )

    result = await engine.execute("query positiveFloatNok { positiveFloat }")
    assert result["data"]["positiveFloat"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "could not convert string to float: 'nope'"
    )


@pytest.mark.asyncio
async def test__positive_float_mutation_ok():
    @Resolver("Mutation.positiveFloat", schema_name="test_positive_float_mutation_ok")
    async def positive_float_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        positiveFloat: PositiveFloat
    }

    type Mutation {
        positiveFloat(input: PositiveFloat): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_float_mutation_ok",
    )

    assert await engine.execute('mutation positiveFloat { positiveFloat(input:100) }') == {
        "data": {"positiveFloat":  True}
    }


@pytest.mark.asyncio
async def test_positive_float_mutation_nok():
    @Resolver("Mutation.positiveFloat", schema_name="test_positive_float_mutation_nok")
    async def positive_float_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        positiveFloat: PositiveFloat
    }

    type Mutation {
        positiveFloat(input: PositiveFloat): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_float_mutation_nok",
    )

    result = await engine.execute('mutation positiveFloat { positiveFloat(input:-100) }')
    assert result['data'] is None
    assert len(result['errors']) == 1
    assert result['errors'][0]['message'] == 'Value -100 is not of correct type PositiveFloat'
