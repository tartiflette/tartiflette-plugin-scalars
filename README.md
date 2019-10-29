# tartiflette-plugin-scalars

Tartiflette plugin providing common scalars : 

```python
sdl = 
"""
type Example {
  email: EmailAddress
}
"""

engine = await create_engine(
    sdl=sdl,
    modules=[
        {
            "name": "tartiflette_plugin_scalars",
            "config": {"email_address": {"enabled": True}}
        }
    ],
    schema_name="test_email_address_ok",
)
```

Implemented scalars:

| Name             | Description                                       |
|------------------|---------------------------------------------------|
| EmailAddress     | Represents an email addresses                     |
| Duration         | Represents a timedelta object                     |
| DateTime         | Represents a date and time object                 |
| NegativeFloat    | Represents a negative floating point number       |
| NegativeInt      | Represents a negative integer                     |
| NonNegativeFloat | Represents a positive or 0 floating point number  |
| NonNegativeInt   | Represents a positive or 0 integer                |
| PositiveFloat    | Represents a positive floating point number       |
| PositiveInt      | Represents a positive integer                     |
| NonPositiveFloat | Represents a negative or 0 floating point number  |
| NonPositiveInt   | Represents a negative or 0 integer                |
| Long             | Represents integers between 0 and 2^63            |
| BigInt           | Represents arbitrary length integers              |
| UnsignedInt      | Represents integers between 0 and 2^32            |
| PhoneNumber      | Represents a phone number                         |
| PostalCode       | Represents a postal code                          |
| URL              | Represents an Uniform Resource Locator            |
| GUID             | Represents a Globally Unique IDentifier           |
| HexColorCode     | Hexadecimal representation of a color             |
| HSL              | Hue, Saturation and Lightness of a color          |
| HSLA             | Hue, Saturation, Lightness and Alpha of a color   |
| RGB              | Red, Green, Blue of a color                       |
| RGBA             | Red, Green, Blue and Alpha of a color             |
| IPv4             | Represents an Internet Protocol version 4 address |
| IPv6             | Represents an Internet Protocol version 6 address |
| MAC              | Represents a Media Access Control address         |
| ISBN             | Represents an International Standard Book Number  |
| Port             | Represents a TCP / UDP port                       |
| USCurrency       | Represents an amount of USD                       |
| JSON             | Represents a JSON value                           |
| JSONObject       | Represents a JSON object                          |