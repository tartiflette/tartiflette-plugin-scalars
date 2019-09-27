import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_phone_number_ok():
    @Resolver("Query.phoneNumber", schema_name="test_phone_number_ok")
    async def phone_number_resolver(*_args, **_kwargs):
        return "+33177351100"

    sdl = """
    type Query {
        phoneNumber: PhoneNumber
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_phone_number_ok",
    )

    assert await engine.execute("query phoneNumberOk { phoneNumber }") == {
        "data": {"phoneNumber": "+33177351100"}
    }


@pytest.mark.asyncio
async def test_phone_number_ok_nok():
    @Resolver("Query.phoneNumber", schema_name="test_phone_number_nok")
    async def phone_number_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        phoneNumber: PhoneNumber
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_phone_number_nok",
    )

    result = await engine.execute("query phoneNumberNok { phoneNumber }")
    assert result["data"]["phoneNumber"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value is not a valid phone number: < nope >"
    )
