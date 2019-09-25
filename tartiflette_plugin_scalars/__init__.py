from importlib import import_module

from tartiflette import Scalar

_SCALAR_TEMPLATE = "scalar {0}"
AVAILABLE_SCALARS = [
    ("email_address", "EmailAddress"),
    ("datetime", "DateTime"),
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
            Scalar(name=scalar_name, schema_name=schema_name)(scalar_class())
            scalars.append(_SCALAR_TEMPLATE.format(scalar_name))

    return scalars


async def bake(schema_name, config):
    return "\n".join(_generate_scalars(schema_name, config))
