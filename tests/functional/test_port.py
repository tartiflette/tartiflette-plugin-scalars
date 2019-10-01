import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_port_ok():
    @Resolver("Query.port", schema_name="test_port_ok")
    async def port_resolver(*_args, **_kwargs):
        return 999

    sdl = """
    type Query {
        port: Port
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_port_ok",
    )

    assert await engine.execute("query portOk { port }") == {
        "data": {"port": 999}
    }


@pytest.mark.asyncio
async def test_port_nok():
    @Resolver("Query.port", schema_name="test_port_nok")
    async def port_resolver(*_args, **_kwargs):
        return -2

    sdl = """
    type Query {
        port: Port
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_port_nok",
    )

    result = await engine.execute("query portNok { port }")
    assert result["data"]["port"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Port cannot represent values below or equal to 0: < -2 >"
    )
