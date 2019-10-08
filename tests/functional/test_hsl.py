import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_hsl_ok():
    @Resolver("Query.hsl", schema_name="test_hsl_ok")
    async def hsl_resolver(*_args, **_kwargs):
        return "hsl(.75turn, 60%, 70%)"

    sdl = """
    type Query {
        hsl: HSL
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsl_ok",
    )

    assert await engine.execute("query hslOk { hsl }") == {
        "data": {"hsl": "hsl(.75turn, 60%, 70%)"}
    }


@pytest.mark.asyncio
async def test_hsl_nok():
    @Resolver("Query.hsl", schema_name="test_hsl_nok")
    async def hsl_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        hsl: HSL
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsl_nok",
    )

    result = await engine.execute("query hslNok { hsl }")
    assert result["data"]["hsl"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"] == "Value is not a valid HSL: < nope >"
    )


@pytest.mark.asyncio
async def test_hsl_mutation_ok():
    @Resolver("Mutation.hsl", schema_name="test_hsl_mutation_ok")
    async def hsl_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        hsl: HSL
    }

    type Mutation {
        hsl(input: HSL): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsl_mutation_ok",
    )

    assert await engine.execute(
        'mutation hsl { hsl(input:"hsl(270, 60%, 50%)") }'
    ) == {"data": {"hsl": True}}


@pytest.mark.asyncio
async def test_hsl_mutation_nok():
    @Resolver("Mutation.hsl", schema_name="test_hsl_mutation_nok")
    async def hsl_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        hsl: HSL
    }

    type Mutation {
        hsl(input: HSL): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hsl_mutation_nok",
    )

    result = await engine.execute('mutation hsl { hsl(input:"nok") }')
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type HSL"
    )
