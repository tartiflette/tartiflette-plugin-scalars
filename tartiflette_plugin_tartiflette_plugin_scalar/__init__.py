from tartiflette import Directive, Scalar, Resolver


_SDL = """
Place your SDL here
"""

# Create your directive/scalar here

async def bake(schema_name, config):
    # Do you magic here, instance and decorate your directive scalar and so on

    return _SDL