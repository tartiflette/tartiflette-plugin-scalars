import datetime

import pytest

from geojson import Point
from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_geojson_ok():
    @Resolver("Query.geojson", schema_name="test_geojson_ok")
    async def geojson_resolver(*_args, **_kwargs):
        return Point((21.56476, 17.39583))

    sdl = """
    type Query {
        geojson: GeoJSON
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_geojson_ok",
    )

    assert await engine.execute("query geoJsonOk { geojson }") == {
        "data": {
            "geojson": '{"coordinates": [21.56476, 17.39583], "type": "Point"}'
        }
    }


@pytest.mark.asyncio
async def test_geojson_nok():
    @Resolver("Query.geojson", schema_name="test_geojson_nok")
    async def geojson_resolver(*_args, **_kwargs):
        return datetime.datetime(2019, 9, 23, 13, 44, 0)

    sdl = """
    type Query {
        geojson: GeoJSON
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_geojson_nok",
    )

    result = await engine.execute("query geojson { geojson }")
    assert result["data"]["geojson"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Object of type datetime is not GeoJSON serializable"
    )


@pytest.mark.asyncio
async def test_geojson_mutation_ok():
    @Resolver("Mutation.geojson", schema_name="test_geojson_mutation_ok")
    async def json_resolver(*_args, **_kwargs):
        return Point((21.56476, 17.39583))

    sdl = """
    type Query {
        geojson: GeoJSON
    }

    type Mutation {
        geojson(input: GeoJSON): GeoJSON
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_geojson_mutation_ok",
    )

    assert await engine.execute(
        'mutation geojson { geojson(input:"true") }'
    ) == {
        "data": {
            "geojson": '{"coordinates": [21.56476, 17.39583], "type": "Point"}'
        }
    }


@pytest.mark.asyncio
async def test_geojson_mutation_nok():
    @Resolver("Mutation.geojson", schema_name="test_geojson_mutation_nok")
    async def geojson_resolver(*_args, **_kwargs):
        return Point((21.56476, 17.39583))

    sdl = """
    type Query {
        geojson: GeoJSON
    }

    type Mutation {
        geojson(input: GeoJSON): GeoJSON
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_geojson_mutation_nok",
    )

    result = await engine.execute("mutation geojson { geojson(input:1) }")
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value 1 is not of correct type GeoJSON"
    )
