import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_guid_ok():
    @Resolver("Query.guid", schema_name="test_guid_ok")
    async def guid_resolver(*_args, **_kwargs):
        return "555b1126-30d9-4354-bc5e-8096e7ce5689"

    sdl = """
    type Query {
        guid: GUID
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_guid_ok",
    )

    assert await engine.execute("query guidOk { guid }") == {
        "data": {"guid": "555b1126-30d9-4354-bc5e-8096e7ce5689"}
    }


@pytest.mark.asyncio
async def test_guid_nok():
    @Resolver("Query.guid", schema_name="test_guid_nok")
    async def guid_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        guid: GUID
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_guid_nok",
    )

    result = await engine.execute("query guidNok { guid }")
    assert result["data"]["guid"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"] == "Value is not a valid GUID: < nope >"
    )


@pytest.mark.asyncio
async def test_guid_mutation_ok():
    @Resolver("Mutation.guid", schema_name="test_guid_mutation_ok")
    async def guid_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        guid: GUID
    }

    type Mutation {
        guid(input: GUID): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_guid_mutation_ok",
    )

    assert await engine.execute('mutation guid { guid(input:"5591b4e9-c747-45ae-8abf-d9cd1a17081e") }') == {
        "data": {"guid":  True}
    }


@pytest.mark.asyncio
async def test_guid_mutation_nok():
    @Resolver("Mutation.guid", schema_name="test_guid_mutation_nok")
    async def guid_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        guid: GUID
    }

    type Mutation {
        guid(input: GUID): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_guid_mutation_nok",
    )

    result = await engine.execute('mutation guid { guid(input:"nok") }')
    assert result['data'] is None
    assert len(result['errors']) == 1
    assert result['errors'][0]['message'] == 'Value nok is not of correct type GUID'
