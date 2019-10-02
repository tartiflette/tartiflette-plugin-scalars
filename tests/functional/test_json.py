import asyncio

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
