from importlib import import_module

from tartiflette import Scalar

_SCALAR_TEMPLATE = "scalar {0}"
AVAILABLE_SCALARS = [
    ("email_address", "EmailAddress"),
    ("datetime", "DateTime"),
    ("naive_datetime", "NaiveDateTime"),
    ("duration", "Duration"),
    ("negative_float", "NegativeFloat"),
    ("negative_int", "NegativeInt"),
    ("non_negative_float", "NonNegativeFloat"),
    ("non_negative_int", "NonNegativeInt"),
    ("non_positive_float", "NonPositiveFloat"),
    ("non_positive_int", "NonPositiveInt"),
    ("positive_float", "PositiveFloat"),
    ("positive_int", "PositiveInt"),
    ("long", "Long"),
    ("big_int", "BigInt"),
    ("unsigned_int", "UnsignedInt"),
    ("phone_number", "PhoneNumber"),
    ("postal_code", "PostalCode"),
    ("url", "URL"),
    ("guid", "GUID"),
    ("uuid", "UUID"),
    ("hex_color_code", "HexColorCode"),
    ("hsl", "HSL"),
    ("hsla", "HSLA"),
    ("rgb", "RGB"),
    ("rgba", "RGBA"),
    ("ipv4", "IPv4"),
    ("ipv6", "IPv6"),
    ("isbn", "ISBN"),
    ("mac", "MAC"),
    ("port", "Port"),
    ("us_currency", "USCurrency"),
    ("json", "JSON"),
    ("json_object", "JSONObject"),
    ("geo_json", "GeoJSON"),
]


def _generate_scalars(schema_name, config):
    scalars = []

    for scalar in AVAILABLE_SCALARS:
        scalar_config = config.get(scalar[0], {})
        if scalar_config.get("enabled") is not False:
            scalar_mod = import_module(
                f"tartiflette_plugin_scalars.{scalar[0]}"
            )
            scalar_class = getattr(scalar_mod, scalar[1])

            scalar_name = scalar_config.get("name") or scalar[1]
            Scalar(name=scalar_name, schema_name=schema_name)(
                scalar_class(**scalar_config.get("options", {}))
            )
            scalars.append(_SCALAR_TEMPLATE.format(scalar_name))

    return scalars


async def bake(schema_name, config):
    return "\n".join(_generate_scalars(schema_name, config))
