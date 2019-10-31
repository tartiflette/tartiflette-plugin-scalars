import pytest

from geojson import (
    Feature,
    FeatureCollection,
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import DirectiveDefinitionNode, StringValueNode

from tartiflette_plugin_scalars.geo_json import GeoJSON


@pytest.mark.parametrize(
    "input_val,exception,output_val",
    [
        (False, TypeError, None),
        ("", ValueError, None),
        ("randomstring", ValueError, None),
        (
            '{"coordinates": [-115.81, 37.24], "type": "Point"}',
            None,
            Point((-115.81, 37.24)),
        ),
        (
            '{"coordinates": [-115.123456123456, 37.123456123456], "type": "Point"}',
            None,
            Point((-115.123456, 37.123456)),
        ),
        (
            '{"coordinates": [-115.12345678, 37.12345678], "type": "Point"}',
            None,
            Point((-115.123457, 37.123457)),
        ),
        (
            '{"coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]], "type": "MultiPoint"}',
            None,
            MultiPoint([(-155.52, 19.61), (-156.22, 20.74), (-157.97, 21.46)]),
        ),
        (
            '{"coordinates": [[8.91, 44.4], [8.92, 44.407]], "type": "LineString"}',
            None,
            LineString([(8.91, 44.4), (8.92, 44.407)]),
        ),
        (
            '{"coordinates": [[[3.73, 9.27], [-130.91, 1.527]], [[23.13, -34.28], [-1.32, -4.69], [3.46, 77.91]]], "type": "MultiLineString"}',
            None,
            MultiLineString(
                [
                    [(3.73, 9.27), (-130.91, 1.527)],
                    [(23.13, -34.28), (-1.32, -4.69), (3.46, 77.91)],
                ]
            ),
        ),
        (
            '{"coordinates": [[[2.36, 57.32], [23.19, -20.2], [-120.48, 19.13]]], "type": "Polygon"}',
            None,
            Polygon([[(2.36, 57.32), (23.19, -20.2), (-120.48, 19.13)]]),
        ),
        (
            '{"coordinates": [[[[3.75, 9.25], [-130.95, 1.55], [35.15, 72.235]]], [[[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]]], "type": "MultiPolygon"}',
            None,
            MultiPolygon(
                [
                    [[(3.75, 9.25), (-130.95, 1.55), (35.15, 72.235)]],
                    [[(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]],
                ]
            ),
        ),
        (
            '{"geometries": [{"coordinates": [23.53, -63.1], "type": "Point"}, {"coordinates": [[-152.6, 51.2], [5.2, 10.6]], "type": "LineString"}], "type": "GeometryCollection"}',
            None,
            GeometryCollection(
                [
                    Point((23.53, -63.1)),
                    LineString([(-152.6, 51.2), (5.2, 10.6)]),
                ]
            ),
        ),
        (
            '{"geometry": {"coordinates": [-3.684, 40.42], "type": "Point"}, "properties": {"key": true}, "type": "Feature"}',
            None,
            Feature(geometry=Point((-3.684, 40.42)), properties={"key": True}),
        ),
        (
            '{"features": [{"geometry": {"coordinates": [1.6433, -19.123], "type": "Point"}, "properties": {"test": "yes"}, "type": "Feature"}, {"geometry": {"coordinates": [-80.233, -22.533], "type": "Point"}, "properties": {"another": "test"}, "type": "Feature"}], "type": "FeatureCollection"}',
            None,
            FeatureCollection(
                [
                    Feature(
                        geometry=Point((1.6433, -19.123)),
                        properties={"test": "yes"},
                    ),
                    Feature(
                        geometry=Point((-80.233, -22.533)),
                        properties={"another": "test"},
                    ),
                ]
            ),
        ),
    ],
)
def test_coerce_input(input_val, exception, output_val):
    scalar = GeoJSON()
    if exception:
        with pytest.raises(exception):
            scalar.coerce_input(input_val)
    else:
        assert scalar.coerce_input(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val",
    [
        (
            Point((-115.81, 37.24)),
            '{"coordinates": [-115.81, 37.24], "type": "Point"}',
        ),
        (
            Point((-115.123456123456, 37.123456123456)),
            '{"coordinates": [-115.123456, 37.123456], "type": "Point"}',
        ),
        (
            Point((-115.123456123456, 37.123456123456), precision=12),
            '{"coordinates": [-115.123456123456, 37.123456123456], "type": "Point"}',
        ),
        (
            MultiPoint([(-155.52, 19.61), (-156.22, 20.74), (-157.97, 21.46)]),
            '{"coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]], "type": "MultiPoint"}',
        ),
        (
            LineString([(8.91, 44.4), (8.92, 44.407)]),
            '{"coordinates": [[8.91, 44.4], [8.92, 44.407]], "type": "LineString"}',
        ),
        (
            MultiLineString(
                [
                    [(3.73, 9.27), (-130.91, 1.527)],
                    [(23.13, -34.28), (-1.32, -4.69), (3.46, 77.91)],
                ]
            ),
            '{"coordinates": [[[3.73, 9.27], [-130.91, 1.527]], [[23.13, -34.28], [-1.32, -4.69], [3.46, 77.91]]], "type": "MultiLineString"}',
        ),
        (
            Polygon([[(2.36, 57.32), (23.19, -20.2), (-120.48, 19.13)]]),
            '{"coordinates": [[[2.36, 57.32], [23.19, -20.2], [-120.48, 19.13]]], "type": "Polygon"}',
        ),
        (
            MultiPolygon(
                [
                    [[(3.75, 9.25), (-130.95, 1.55), (35.15, 72.235)]],
                    [[(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]],
                ]
            ),
            '{"coordinates": [[[[3.75, 9.25], [-130.95, 1.55], [35.15, 72.235]]], [[[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]]], "type": "MultiPolygon"}',
        ),
        (
            GeometryCollection(
                [
                    Point((23.532, -63.12)),
                    LineString([(-152.62, 51.22), (5.22, 12.62)]),
                ]
            ),
            '{"geometries": [{"coordinates": [23.532, -63.12], "type": "Point"}, {"coordinates": [[-152.62, 51.22], [5.22, 12.62]], "type": "LineString"}], "type": "GeometryCollection"}',
        ),
        (
            Feature(geometry=Point((-3.684, 40.42)), properties={"key": True}),
            '{"geometry": {"coordinates": [-3.684, 40.42], "type": "Point"}, "properties": {"key": true}, "type": "Feature"}',
        ),
        (
            FeatureCollection(
                [
                    Feature(
                        geometry=Point((1.6433, -19.123)),
                        properties={"test": "yes"},
                    ),
                    Feature(
                        geometry=Point((-80.233, -22.533)),
                        properties={"another": "test"},
                    ),
                ]
            ),
            '{"features": [{"geometry": {"coordinates": [1.6433, -19.123], "type": "Point"}, "properties": {"test": "yes"}, "type": "Feature"}, {"geometry": {"coordinates": [-80.233, -22.533], "type": "Point"}, "properties": {"another": "test"}, "type": "Feature"}], "type": "FeatureCollection"}',
        ),
    ],
)
def test_coerce_output(input_val, output_val):
    scalar = GeoJSON()
    assert scalar.coerce_output(input_val) == output_val


@pytest.mark.parametrize(
    "input_val,output_val",
    [
        (
            DirectiveDefinitionNode(
                arguments=[], name="directive", locations=None
            ),
            UNDEFINED_VALUE,
        ),
        (
            StringValueNode(
                value='{"coordinates": [-115.81, 37.24], "type": "Point"}'
            ),
            {"coordinates": [-115.81, 37.24], "type": "Point"},
        ),
    ],
)
def test_parse_literal(input_val, output_val):
    assert GeoJSON().parse_literal(input_val) == output_val
