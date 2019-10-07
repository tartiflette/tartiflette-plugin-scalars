import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_hsla_ok():
    @Resolver("Query.hsla", schema_name="test_hsla_ok")
    async def hsla_resolver(*_args, **_kwargs):
        return "hsla(.75turn, 60%, 70%, .5)"

    sdl = """
    type Query {
        hsla: HSLA
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsla_ok",
    )

    assert await engine.execute("query hslaOk { hsla }") == {
        "data": {"hsla": "hsla(.75turn, 60%, 70%, .5)"}
    }


@pytest.mark.asyncio
async def test_hsla_nok():
    @Resolver("Query.hsla", schema_name="test_hsla_nok")
    async def hsla_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        hsla: HSLA
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsla_nok",
    )

    result = await engine.execute("query hslaNok { hsla }")
    assert result["data"]["hsla"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"] == "Value is not a valid HSLA: < nope >"
    )


@pytest.mark.asyncio
async def test_hsla_mutation_ok():
    @Resolver("Mutation.hsla", schema_name="test_hsla_mutation_ok")
    async def hsla_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        hsla: HSLA
    }

    type Mutation {
        hsla(input: HSLA): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsla_mutation_ok",
    )

    assert await engine.execute(
        'mutation hsla { hsla(input:"hsla(270, 60%, 50%, .5)") }'
    ) == {"data": {"hsla": True}}


@pytest.mark.asyncio
async def test_hsla_mutation_nok():
    @Resolver("Mutation.hsla", schema_name="test_hsla_mutation_nok")
    async def hsla_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        hsla: HSLA
    }

    type Mutation {
        hsla(input: HSLA): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsla_mutation_nok",
    )

    result = await engine.execute('mutation hsla { hsla(input:"nok") }')
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type HSLA"
    )
