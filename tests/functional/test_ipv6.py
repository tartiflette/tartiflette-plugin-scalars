import asyncio
import ipaddress

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_ipv6_ok():
    @Resolver("Query.ipv6", schema_name="test_ipv6_ok")
    async def ipv6_resolver(*_args, **_kwargs):
        return ipaddress.ip_address("::1")

    sdl = """
    type Query {
        ipv6: IPv6
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_ipv6_ok",
    )

    assert await engine.execute("query ipv6Ok { ipv6 }") == {
        "data": {"ipv6": "::1"}
    }


@pytest.mark.asyncio
async def test_ipv6_ok_nok():
    @Resolver("Query.ipv6", schema_name="test_ipv6_nok")
    async def ipv6_resolver(*_args, **_kwargs):
        return "nok"

    sdl = """
    type Query {
        ipv6: IPv6
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_ipv6_nok",
    )

    result = await engine.execute("query ipv6Nok { ipv6 }")
    assert result["data"]["ipv6"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "IPv6 cannot represent value: < nok >"
    )


@pytest.mark.asyncio
async def test_ipv6_mutation_ok():
    @Resolver("Mutation.ipv6", schema_name="test_ipv6_mutation_ok")
    async def ipv6_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        ipv6: IPv6
    }

    type Mutation {
        ipv6(input: IPv6): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_ipv6_mutation_ok",
    )

    assert await engine.execute(
        'mutation ipv6 { ipv6(input:"2001:0db8:0000:0000:0000:8a2e:0370:7334") }'
    ) == {"data": {"ipv6": True}}


@pytest.mark.asyncio
async def test_ipv6_mutation_nok():
    @Resolver("Mutation.ipv6", schema_name="test_ipv6_mutation_nok")
    async def ipv6_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        ipv6: IPv6
    }

    type Mutation {
        ipv6(input: IPv6): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_ipv6_mutation_nok",
    )

    result = await engine.execute('mutation ipv6 { ipv6(input:"nok") }')
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type IPv6"
    )
