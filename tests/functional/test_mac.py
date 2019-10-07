import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_mac_ok():
    @Resolver("Query.mac", schema_name="test_mac_ok")
    async def mac_resolver(*_args, **_kwargs):
        return "00:0a:95:9d:68:16"

    sdl = """
    type Query {
        mac: MAC
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_mac_ok",
    )

    assert await engine.execute("query mac { mac }") == {
        "data": {"mac": "00:0a:95:9d:68:16"}
    }


@pytest.mark.asyncio
async def test_mac_nok():
    @Resolver("Query.mac", schema_name="test_mac_nok")
    async def mac_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        mac: MAC
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_mac_nok",
    )

    result = await engine.execute("query mac { mac }")
    assert result["data"]["mac"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value is not a valid MAC address: < nope >"
    )


@pytest.mark.asyncio
async def test_mac_mutation_ok():
    @Resolver("Mutation.mac", schema_name="test_mac_mutation_ok")
    async def mac_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        mac: MAC
    }

    type Mutation {
        mac(input: MAC): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_mac_mutation_ok",
    )

    assert await engine.execute('mutation mac { mac(input:"00:0a:95:9d:68:16") }') == {
        "data": {"mac":  True}
    }


@pytest.mark.asyncio
async def test_mac_mutation_nok():
    @Resolver("Mutation.mac", schema_name="test_mac_mutation_nok")
    async def mac_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        mac: MAC
    }

    type Mutation {
        mac(input: MAC): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_mac_mutation_nok",
    )

    result = await engine.execute('mutation mac { mac(input:"nok") }')
    assert result['data'] is None
    assert len(result['errors']) == 1
    assert result['errors'][0]['message'] == 'Value nok is not of correct type MAC'
