import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_json_object_ok():
    @Resolver("Query.jsonObject", schema_name="test_json_object_ok")
    async def json_object_resolver(*_args, **_kwargs):
        return {"key": "value"}

    sdl = """
    type Query {
        jsonObject: JSONObject
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_object_ok",
    )

    assert await engine.execute("query jsonObjectOk { jsonObject }") == {
        "data": {"jsonObject": '{"key": "value"}'}
    }


@pytest.mark.asyncio
async def test_json_object_nok():
    @Resolver("Query.jsonObject", schema_name="test_json_object_nok")
    async def json_object_resolver(*_args, **_kwargs):
        return "nok"

    sdl = """
    type Query {
        jsonObject: JSONObject
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_object_nok",
    )

    result = await engine.execute("query jsonObjectNok { jsonObject }")
    assert result["data"]["jsonObject"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "JSONObject cannot represent value: < nok >"
    )


@pytest.mark.asyncio
async def test_json_object_mutation_ok():
    @Resolver(
        "Mutation.jsonObject", schema_name="test_json_object_mutation_ok"
    )
    async def json_object_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        jsonObject: JSONObject
    }

    type Mutation {
        jsonObject(input: JSONObject): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_object_mutation_ok",
    )

    assert await engine.execute(
        """mutation jsonObject { jsonObject(input:"{\\\"ok\\\": 2}") }"""
    ) == {"data": {"jsonObject": True}}


@pytest.mark.asyncio
async def test_json_object_mutation_nok():
    @Resolver(
        "Mutation.jsonObject", schema_name="test_json_object_mutation_nok"
    )
    async def json_object_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        jsonObject: JSONObject
    }

    type Mutation {
        jsonObject(input: JSONObject): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_json_object_mutation_nok",
    )

    result = await engine.execute(
        'mutation jsonObject { jsonObject(input:"nok") }'
    )
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type JSONObject"
    )
