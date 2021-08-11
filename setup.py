from setuptools import find_packages, setup

_TEST_REQUIRE = [
    "pytest==6.2.4",
    "pytest-cov==2.12.1",
    "pytest-asyncio==0.15.1",
    "pylint==2.9.6",
    "black==21.7b0",
    "isort==5.9.3",
]

_VERSION = "0.3.1"

_PACKAGES = find_packages(exclude=["tests*"])


def _read_file(filename):
    with open(filename) as afile:
        return afile.read()


setup(
    name="tartiflette-plugin-scalars",
    version=_VERSION,
    description="Tartiflette plugin providing common scalars",
    long_description=_read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/dailymotion/tartiflette-plugin-scalars",
    author="Alice Girard Guittard",
    author_email="alice.girardguittard@dailymotion.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="api graphql protocol tartiflette",
    packages=_PACKAGES,
    install_requires=[
        "tartiflette>=1.0.0,<2.0.0",
        "python-dateutil==2.8.2",
        "geojson==2.5.0",
    ],
    tests_require=_TEST_REQUIRE,
    extras_require={"test": _TEST_REQUIRE},
    include_package_data=True,
)
