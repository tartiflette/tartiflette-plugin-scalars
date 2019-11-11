# tartiflette-plugin-scalars

Tartiflette plugin providing common scalars, for data validation and strongly typed API schemas.

## Requirements

Python >= 3.6
Tartiflette >= 1.0.0

## Installation

Simply install it with pip:

```
pip install tartiflette-plugin-scalars
```

Then start coding, by importing adding it to the modules list of tartiflette's create engine:

```python
import asyncio
import datetime

from tartiflette import Resolver, create_engine

async def main():
    sdl = """
    type Query {
      dateTime: DateTime
    }
    """

    @Resolver("Query.dateTime", schema_name="scalars")
    async def resolve_date_time(*_args, **_kwargs):
        return datetime.datetime(2019, 10, 29, 20, 23, 00, 00)

    engine = await create_engine(
        sdl=sdl,
        modules=[
            {
                "name": "tartiflette_plugin_scalars",
                "config": {"datetime": {"enabled": True}}
            }
        ],
        schema_name="scalars",
    )

    print(await engine.execute("query date { dateTime }"))


asyncio.run(main())
```

## Configuration

You can configure the plugin by passing a configuration dict during create_engine.
This configuration can be used to disable or rename some scalars, as shown below:

```
engine = await create_engine(
    sdl=sdl,
    modules=[
        {
            "name": "tartiflette_plugin_scalars",
            "config": {
                "datetime": {"name": "MyDatetime"},
                "postal_code": {"enabled": False},
            },
        }
    ],
    schema_name="scalars",
)
```

Some plugins also accept more specific configuration values, that can be
specified in a sub-dict called `options`. The options will be
passed to the scalar at instanciation time as `**kwargs` to the `init()` method.

```
engine = await create_engine(
    sdl=sdl,
    modules=[
        {
            "name": "tartiflette_plugin_scalars",
            "config": {
                "datetime": {"name": "MyDatetime"},
                "postal_code": {"enabled": False, "options": {"key": "value"}},
            },
        }
    ],
    schema_name="scalars",
)
```

## Implemented scalars:

| Name                                   | Configuration key  | Description                                       |
|----------------------------------------|--------------------|---------------------------------------------------|
| EmailAddress                           | email_address      | Represents an email addresses                     |
| DateTime                               | datetime           | Represents a date and time object                 |
| Duration                               | duration           | Represents a timedelta object                     |
| NegativeFloat                          | negative_float     | Represents a negative floating point number       |
| NegativeInt                            | negative_int       | Represents a negative integer                     |
| NonNegativeFloat                       | non_negative_float | Represents a positive or 0 floating point number  |
| NonNegativeInt                         | non_negative_int   | Represents a positive or 0 integer                |
| PositiveFloat                          | positive_float     | Represents a positive floating point number       |
| PositiveInt                            | positive_int       | Represents a positive integer                     |
| NonPositiveFloat                       | non_positive_float | Represents a negative or 0 floating point number  |
| NonPositiveInt                         | non_positive_int   | Represents a negative or 0 integer                |
| Long                                   | long               | Represents integers between 0 and 2^63            |
| BigInt                                 | big_int            | Represents arbitrary length integers              |
| UnsignedInt                            | unsigned_int       | Represents integers between 0 and 2^32            |
| PhoneNumber                            | phone_number       | Represents a phone number                         |
| PostalCode                             | postal_code        | Represents a postal code                          |
| URL                                    | url                | Represents an Uniform Resource Locator            |
| GUID                                   | guid               | Represents a Globally Unique IDentifier           |
| HexColorCode                           | hex_color_code     | Hexadecimal representation of a color             |
| HSL                                    | hsl                | Hue, Saturation and Lightness of a color          |
| HSLA                                   | hsla               | Hue, Saturation, Lightness and Alpha of a color   |
| RGB                                    | rgb                | Red, Green, Blue of a color                       |
| RGBA                                   | rgba               | Red, Green, Blue and Alpha of a color             |
| IPv4                                   | ipv4               | Represents an Internet Protocol version 4 address |
| IPv6                                   | ipv6               | Represents an Internet Protocol version 6 address |
| MAC                                    | mac                | Represents a Media Access Control address         |
| ISBN                                   | isbn               | Represents an International Standard Book Number  |
| Port                                   | port               | Represents a TCP / UDP port                       |
| USCurrency                             | us_currency        | Represents an amount of USD                       |
| JSON                                   | json               | Represents a JSON value                           |
| JSONObject                             | json_object        | Represents a JSON object                          |
| [GeoJSON](./docs/geo_json.md)          | geo_json           | Represents a GeoJSON value                        |
