import asyncio

from urllib.parse import ParseResult

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_url_ok():
    @Resolver("Query.url", schema_name="test_url_ok")
    async def url_resolver(*_args, **_kwargs):
        return ParseResult(
            scheme="https",
            netloc="www.dailymotion.com",
            path="/play",
            params="",
            query="",
            fragment="",
        )

    sdl = """
    type Query {
        url: URL
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_url_ok",
    )

    assert await engine.execute("query urlOk { url }") == {
        "data": {"url": "https://www.dailymotion.com/play"}
    }


@pytest.mark.asyncio
async def test_url_nok():
    @Resolver("Query.url", schema_name="test_url_nok")
    async def url_resolver(*_args, **_kwargs):
        return ParseResult(
            scheme="", netloc="", path="", params="", query="", fragment=""
        )

    sdl = """
    type Query {
        url: URL
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_url_nok",
    )

    result = await engine.execute("query urlNok { url }")
    assert result["data"]["url"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "URL cannot represent value: < ParseResult(scheme='', netloc='', path='', params='', query='', fragment='') >"
    )
