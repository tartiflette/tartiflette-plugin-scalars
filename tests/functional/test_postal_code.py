import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_postal_code_ok():
    @Resolver("Query.postalCode", schema_name="test_postal_code_ok")
    async def postal_code_resolver(*_args, **_kwargs):
        return "75017"

    sdl = """
    type Query {
        postalCode: PostalCode
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_postal_code_ok",
    )

    assert await engine.execute("query postalCodeOk { postalCode }") == {
        "data": {"postalCode": "75017"}
    }


@pytest.mark.asyncio
async def test_postal_code_ok_nok():
    @Resolver("Query.postalCode", schema_name="test_postal_code_nok")
    async def postal_code_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        postalCode: PostalCode
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_postal_code_nok",
    )

    result = await engine.execute("query postalCodeNok { postalCode }")
    assert result["data"]["postalCode"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value is not a valid postal code: < nope >"
    )
