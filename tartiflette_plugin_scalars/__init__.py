from tartiflette import Scalar

_SCALAR_TEMPLATE = "scalar {0}"


async def bake(schema_name, config):
    scalars = []

    email_address_config = config.get("email_address", {})
    if email_address_config.get("enabled") is not False:
        from tartiflette_plugin_scalars.email_address import EmailAddress

        email_address_name = email_address_config.get("name") or "EmailAddress"
        Scalar(name=email_address_name, schema_name=schema_name)(
            EmailAddress()
        )
        scalars.append(_SCALAR_TEMPLATE.format(email_address_name))

    return "\n".join(scalars)
