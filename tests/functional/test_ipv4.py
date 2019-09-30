import asyncio
import ipaddress

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_ipv4_ok():
    @Resolver("Query.ipv4", schema_name="test_ipv4_ok")
    async def ipv4_resolver(*_args, **_kwargs):
        return ipaddress.ip_address("127.0.0.1")

    sdl = """
    type Query {
        ipv4: IPv4
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_ipv4_ok",
    )

    assert await engine.execute("query ipv4Ok { ipv4 }") == {
        "data": {"ipv4": "127.0.0.1"}
    }


@pytest.mark.asyncio
async def test_ipv4_ok_nok():
    @Resolver("Query.ipv4", schema_name="test_ipv4_nok")
    async def ipv4_resolver(*_args, **_kwargs):
        return "nok"

    sdl = """
    type Query {
        ipv4: IPv4
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_ipv4_nok",
    )

    result = await engine.execute("query ipv4Nok { ipv4 }")
    assert result["data"]["ipv4"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "IPv4 cannot represent value: < nok >"
    )
