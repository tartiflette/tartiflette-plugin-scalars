import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_isbn_ok():
    @Resolver("Query.isbn", schema_name="test_isbn_ok")
    async def isbn_resolver(*_args, **_kwargs):
        return "ISBN 0-06-059518-3"

    sdl = """
    type Query {
        isbn: ISBN
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_isbn_ok",
    )

    assert await engine.execute("query isbnOk { isbn }") == {
        "data": {"isbn": "ISBN 0-06-059518-3"}
    }


@pytest.mark.asyncio
async def test_isbn_ok_nok():
    @Resolver("Query.isbn", schema_name="test_isbn_nok")
    async def isbn_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        isbn: ISBN
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_isbn_nok",
    )

    result = await engine.execute("query isbnNok { isbn }")
    assert result["data"]["isbn"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"] == "Value is not a valid ISBN: < nope >"
    )


@pytest.mark.asyncio
async def test_isbn_mutation_ok():
    @Resolver("Mutation.isbn", schema_name="test_isbn_mutation_ok")
    async def isbn_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        isbn: ISBN
    }

    type Mutation {
        isbn(input: ISBN): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_isbn_mutation_ok",
    )

    assert await engine.execute(
        'mutation isbn { isbn(input:"ISBN 0-9630096-0-5") }'
    ) == {"data": {"isbn": True}}


@pytest.mark.asyncio
async def test_isbn_mutation_nok():
    @Resolver("Mutation.isbn", schema_name="test_isbn_mutation_nok")
    async def isbn_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        isbn: ISBN
    }

    type Mutation {
        isbn(input: ISBN): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_isbn_mutation_nok",
    )

    result = await engine.execute('mutation isbn { isbn(input:"nok") }')
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type ISBN"
    )
