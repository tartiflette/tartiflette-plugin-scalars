import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_us_currency_ok():
    @Resolver("Query.usCurrency", schema_name="test_us_currency_ok")
    async def us_currency_resolver(*_args, **_kwargs):
        return 10050

    sdl = """
    type Query {
        usCurrency: USCurrency
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_us_currency_ok",
    )

    assert await engine.execute("query usCurrencyOk { usCurrency }") == {
        "data": {"usCurrency": "$100.50"}
    }


@pytest.mark.asyncio
async def test_us_currency_nok():
    @Resolver("Query.usCurrency", schema_name="test_us_currency_nok")
    async def us_currency_resolver(*_args, **_kwargs):
        return "nok"

    sdl = """
    type Query {
        usCurrency: USCurrency
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_us_currency_nok",
    )

    result = await engine.execute("query usCurrencyNok { usCurrency }")
    assert result["data"]["usCurrency"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "USCurrency cannot represent value: < nok >"
    )


@pytest.mark.asyncio
async def test_us_currency_mutation_ok():
    @Resolver(
        "Mutation.usCurrency", schema_name="test_us_currency_mutation_ok"
    )
    async def us_currency_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        usCurrency: USCurrency
    }

    type Mutation {
        usCurrency(input: USCurrency): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_us_currency_mutation_ok",
    )

    assert await engine.execute(
        'mutation usCurrency { usCurrency(input:"75017") }'
    ) == {"data": {"usCurrency": True}}


@pytest.mark.asyncio
async def test_us_currency_mutation_nok():
    @Resolver(
        "Mutation.usCurrency", schema_name="test_us_currency_mutation_nok"
    )
    async def us_currency_resolver(*_args, **_kwargs):
        return True

    sdl = """
    type Query {
        usCurrency: USCurrency
    }

    type Mutation {
        usCurrency(input: USCurrency): Boolean
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_us_currency_mutation_nok",
    )

    result = await engine.execute(
        'mutation usCurrency { usCurrency(input:"nok") }'
    )
    assert result["data"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value nok is not of correct type USCurrency"
    )
