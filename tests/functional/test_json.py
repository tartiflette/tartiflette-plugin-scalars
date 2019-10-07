import asyncio
import datetime

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_json_ok():
    @Resolver("Query.json", schema_name="test_json_ok")
    async def json_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        json: JSON
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_ok",
    )

    assert await engine.execute("query jsonOk { json }") == {
        "data": {"json": "true"}
    }


@pytest.mark.asyncio
async def test_json_nok():
    @Resolver("Query.json", schema_name="test_json_nok")
    async def json_resolver(*_args, **_kwargs):
        return datetime.datetime(2019, 9, 23, 13, 44, 0)

    sdl = """
    type Query {
        json: JSON
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_nok",
    )

    result = await engine.execute("query json { json }")
    assert result["data"]["json"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Object of type 'datetime' is not JSON serializable"
    )


@pytest.mark.asyncio
async def test_json_mutation_ok():
    @Resolver("Mutation.json", schema_name="test_json_mutation_ok")
    async def json_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        json: JSON
    }

    type Mutation {
        json(input: JSON): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_mutation_ok",
    )

    assert await engine.execute('mutation json { json(input:"true") }') == {
        "data": {"json":  True}
    }


@pytest.mark.asyncio
async def test_json_mutation_nok():
    @Resolver("Mutation.json", schema_name="test_json_mutation_nok")
    async def json_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        json: JSON
    }

    type Mutation {
        json(input: JSON): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_mutation_nok",
    )

    result = await engine.execute('mutation json { json(input:1) }')
    assert result['data'] is None
    assert len(result['errors']) == 1
    assert result['errors'][0]['message'] == 'Value 1 is not of correct type JSON'
