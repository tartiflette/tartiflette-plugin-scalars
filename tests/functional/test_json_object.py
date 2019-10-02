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
async def test_us_curency_nok():
    @Resolver("Query.jsonObject", schema_name="test_json_object_nok")
    async def us_currency_resolver(*_args, **_kwargs):
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
