# PYTHON
from datetime import timedelta

# PYTEST
import pytest

# TARTIFLETTE
from tartiflette import Resolver, create_engine


# duration query ok
@pytest.mark.asyncio
async def test_duration_q_ok():
    @Resolver("Query.duration", schema_name="test_duration_query_ok")
    async def duration_query_resolver(*args, **kwargs):
        return timedelta(days=1)

    sdl = """
    type Query{
        duration: Duration
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_duration_query_ok",
    )

    result = await engine.execute("{duration}")
    assert result == {"data": {"duration": "1 day, 0:00:00"}}


# duration query nok
@pytest.mark.asyncio
async def test_duration_q_nok():
    @Resolver("Query.duration", schema_name="test_duration_query_nok")
    async def duration_query_resolver(*args, **kwargs):
        return "nok"

    sdl = """
        type Query{
            duration: Duration
        }
        """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_duration_query_nok",
    )

    result = await engine.execute("{duration}")

    assert result["data"]["duration"] is None
    assert len(result["errors"]) == 1
    assert result["errors"][0]["message"] == "Duration cannot represent value: < nok >"


# duration mutation ok
@pytest.mark.asyncio
async def test_duration_m_ok():
    @Resolver("Mutation.duration", schema_name="test_duration_mutation_ok")
    async def duration_mutation_resolver(*args, **kwargs):
        return True

    sdl = """
    type Query{
        duration: Duration
    }
    
    type Mutation{
        duration(input: Duration): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_duration_mutation_ok",
    )

    result = await engine.execute(
        """mutation durationTest{duration(input: "days=1")}"""
    )
    assert result == {"data": {"duration": True}}


# duration mutuation nok
@pytest.mark.asyncio
async def test_duration_m_nok():
    @Resolver("Mutation.duration", schema_name="test_duration_mutation_nok")
    async def duration_mutation_resolver(*args, **kwargs):
        return "nok"

    sdl = """
    type Query{
        duration: Duration
    }
    
    type Mutation{
        duration(input: Duration): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_duration_mutation_nok",
    )

    result = await engine.execute("""mutation durationTest{duration(input: "nok")}""")

    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert result["errors"][0]["message"] == "Value nok is not of correct type Duration"
