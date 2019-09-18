import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_email_address_ok():
    @Resolver("Query.email", schema_name="test_email_address_ok")
    async def email_resolver(*_args, **_kwargs):
        return "alice.girardguittard@dm.com"

    sdl = """
    type Query {
        email: EmailAddress
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_email_address_ok",
    )

    assert await engine.execute("query email { email }") == {
        "data": {"email": "alice.girardguittard@dm.com"}
    }


@pytest.mark.asyncio
async def test_email_address_nok():
    @Resolver("Query.email", schema_name="test_email_address_nok")
    async def email_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        email: EmailAddress
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_email_address_nok",
    )

    result = await engine.execute("query email { email }")
    assert result["data"]["email"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value is not a valid email address: < nope >"
    )
