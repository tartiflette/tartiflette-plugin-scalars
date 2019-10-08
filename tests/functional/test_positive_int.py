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


@pytest.mark.asyncio
async def test_positive_int_mutation_ok():
    @Resolver(
        "Mutation.positiveInt", schema_name="test_positive_int_mutation_ok"
    )
    async def positive_int_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        positiveInt: PositiveInt
    }

    type Mutation {
        positiveInt(input: PositiveInt): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_int_mutation_ok",
    )

    assert await engine.execute(
        "mutation positiveInt { positiveInt(input:100) }"
    ) == {"data": {"positiveInt": True}}


@pytest.mark.asyncio
async def test_positive_int_mutation_nok():
    @Resolver(
        "Mutation.positiveInt", schema_name="test_positive_int_mutation_nok"
    )
    async def positive_int_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        positiveInt: PositiveInt
    }

    type Mutation {
        positiveInt(input: PositiveInt): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_positive_int_mutation_nok",
    )

    result = await engine.execute(
        "mutation positiveInt { positiveInt(input:-100) }"
    )
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value -100 is not of correct type PositiveInt"
    )
