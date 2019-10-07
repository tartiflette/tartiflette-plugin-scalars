import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_non_positive_float_ok():
    @Resolver(
        "Query.nonPositiveFloat", schema_name="test_non_positive_float_ok"
    )
    async def non_positive_float_resolver(*_args, **_kwargs):
        return -999.99

    sdl = """
    type Query {
        nonPositiveFloat: NegativeFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_positive_float_ok",
    )

    assert await engine.execute(
        "query nonPositiveFloatOk { nonPositiveFloat }"
    ) == {"data": {"nonPositiveFloat": -999.99}}


@pytest.mark.asyncio
async def test_non_positive_float_nok():
    @Resolver(
        "Query.nonPositiveFloat", schema_name="test_non_positive_float_nok"
    )
    async def non_positive_float_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        nonPositiveFloat: NegativeFloat
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_positive_float_nok",
    )

    result = await engine.execute(
        "query nonPositiveFloatNok { nonPositiveFloat }"
    )
    assert result["data"]["nonPositiveFloat"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "could not convert string to float: 'nope'"
    )


@pytest.mark.asyncio
async def test_non_positive_float_mutation_ok():
    @Resolver("Mutation.nonPositiveFloat", schema_name="test_non_positive_float_mutation_ok")
    async def non_positive_float_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        nonPositiveFloat: NonPositiveFloat
    }

    type Mutation {
        nonPositiveFloat(input: NonPositiveFloat): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_positive_float_mutation_ok",
    )

    assert await engine.execute('mutation nonPositiveFloat { nonPositiveFloat(input:-100) }') == {
        "data": {"nonPositiveFloat":  True}
    }


@pytest.mark.asyncio
async def test_non_positive_float_mutation_nok():
    @Resolver("Mutation.nonPositiveFloat", schema_name="test_non_positive_float_mutation_nok")
    async def non_positive_float_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        nonPositiveFloat: NonPositiveFloat
    }

    type Mutation {
        nonPositiveFloat(input: NonPositiveFloat): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_non_positive_float_mutation_nok",
    )

    result = await engine.execute('mutation nonPositiveFloat { nonPositiveFloat(input:100) }')
    assert result['data'] is None
    assert len(result['errors']) == 1
    assert result['errors'][0]['message'] == 'Value 100 is not of correct type NonPositiveFloat'
