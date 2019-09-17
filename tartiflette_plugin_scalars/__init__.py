from tartiflette import Scalar

from tartiflette_plugin_scalars.email_address import EmailAddress

_SDL = """
scalar EmailAddress
"""


async def bake(schema_name, config):
    Scalar(name="EmailAddress", schema_name=schema_name)(EmailAddress())
    return _SDL
