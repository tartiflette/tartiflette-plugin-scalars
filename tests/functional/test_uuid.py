import uuid

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_uuid_ok():
    @Resolver("Query.uuid", schema_name="test_uuid_ok")
    async def uuid_resolver(*_args, **_kwargs):
        return uuid.UUID("b83f5672-a92a-4937-9c23-de8f2e1c2cf6")

    sdl = """
    type Query {
        uuid: UUID
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_uuid_ok",
    )

    assert await engine.execute("query uuidOk { uuid }") == {
        "data": {"uuid": "b83f5672-a92a-4937-9c23-de8f2e1c2cf6"}
    }


@pytest.mark.asyncio
async def test_uuid_nok():
    @Resolver("Query.uuid", schema_name="test_uuid_nok")
    async def uuid_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        uuid: UUID
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_uuid_nok",
    )

    result = await engine.execute("query uuidNok { uuid }")
    assert result["data"]["uuid"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value is not instance of UUID: < nope >"
    )


@pytest.mark.asyncio
async def test_uuid_mutation_ok():
    @Resolver("Mutation.uuid", schema_name="test_uuid_mutation_ok")
    async def uuid_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        uuid: UUID
    }

    type Mutation {
        uuid(input: UUID): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_uuid_mutation_ok",
    )

    assert await engine.execute(
        'mutation uuid { uuid(input: "5591b4e9-c747-45ae-8abf-d9cd1a17081e") }'
    ) == {"data": {"uuid": True}}


@pytest.mark.asyncio
async def test_uuid_mutation_nok():
    @Resolver("Mutation.uuid", schema_name="test_uuid_mutation_nok")
    async def uuid_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        uuid: UUID
    }

    type Mutation {
        uuid(input: UUID): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_uuid_mutation_nok",
    )

    result = await engine.execute('mutation uuid { uuid(input:"nok") }')
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type UUID"
    )
