import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_long_ok():
    @Resolver("Query.long", schema_name="test_long_ok")
    async def long_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        long: Long
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_long_ok",
    )

    assert await engine.execute("query longOk { long }") == {
        "data": {"long": 999}
    }


@pytest.mark.asyncio
async def test_long_nok():
    @Resolver("Query.long", schema_name="test_long_nok")
    async def long_resolver(*_args, **_kwargs):
        return 2 ** 64

    sdl = """
    type Query {
        long: Long
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_long_nok",
    )

    result = await engine.execute("query longNok { long }")
    assert result["data"]["long"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Long cannot represent values above or equal to 2^63: < 18446744073709551616 >"
    )


@pytest.mark.asyncio
async def test_long_mutation_ok():
    @Resolver("Mutation.long", schema_name="test_long_mutation_ok")
    async def long_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        long: Long
    }

    type Mutation {
        long(input: Long): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_long_mutation_ok",
    )

    assert await engine.execute("mutation long { long(input:100) }") == {
        "data": {"long": True}
    }


@pytest.mark.asyncio
async def test_long_mutation_nok():
    @Resolver("Mutation.long", schema_name="test_long_mutation_nok")
    async def long_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        long: Long
    }

    type Mutation {
        long(input: Long): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_long_mutation_nok",
    )

    result = await engine.execute(
        "mutation long { long(input:9223372036854775809) }"
    )
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value 9223372036854775809 is not of correct type Long"
    )
