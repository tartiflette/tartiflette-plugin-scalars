from datetime import datetime

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_datetime_ok():
    @Resolver("Query.date", schema_name="test_datetime_ok")
    async def date_resolver(*_args, **_kwargs):
        return datetime(2019, 9, 23, 13, 44, 0)

    sdl = """
    type Query {
        date: DateTime
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_datetime_ok",
    )

    assert await engine.execute("query date { date }") == {
        "data": {"date": "2019-09-23T13:44:00"}
    }


@pytest.mark.asyncio
async def test_datetime_nok():
    @Resolver("Query.date", schema_name="test_datetime_nok")
    async def date_resolver(*_args, **_kwargs):
        return "nok"

    sdl = """
    type Query {
        date: DateTime
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_datetime_nok",
    )

    result = await engine.execute("query date { date }")
    assert result["data"]["date"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "DateTime cannot represent value: < nok >"
    )


@pytest.mark.asyncio
async def test_datetime_mutation_ok():
    @Resolver("Mutation.dateTime", schema_name="test_datetime_mutation_ok")
    async def date_time_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        dateTime: DateTime
    }

    type Mutation {
        dateTime(input: DateTime): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_datetime_mutation_ok",
    )

    assert await engine.execute(
        'mutation dateTime { dateTime(input:"2019-10-07T15:02:00+00:00") }'
    ) == {"data": {"dateTime": True}}


@pytest.mark.asyncio
async def test_date_time_mutation_nok():
    @Resolver("Mutation.dateTime", schema_name="test_date_time_mutation_nok")
    async def dateTime_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        dateTime: DateTime
    }

    type Mutation {
        dateTime(input: DateTime): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_datetime_mutation_nok",
    )

    result = await engine.execute(
        'mutation dateTime { dateTime(input:"nok") }'
    )
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type DateTime"
    )
