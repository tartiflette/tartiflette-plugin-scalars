GeoJSON
=======

This scalar wraps the [geojson](https://pypi.org/project/geojson/)
python library. It allows manipulation of GeoJSON data types:

  * Point
  * MultiPoint
  * LineString
  * MultiLineString
  * Polygon
  * MultiPolygon
  * GeometryCollection
  * Feature
  * FeatureCollection

## Precision
The `geojson` lib supports specifying precision on the python objects. For
example:

```
>>> from geojson import Point
>>> import geojson
>>> p = Point((-115.12345678, 58.12345678), precision=8)
>>> geojson.dumps(p)
'{"type": "Point", "coordinates": [-115.12345678, 58.12345678]}'
```

The opposite is not true. You can't specify the GeoJSON to python object
precision (it gets truncated to 6 by default), for now:

```
>>> from geojson import Point
>>> import geojson
>>> geojson.loads('{"type": "Point", "coordinates": [-115.12345678, 58.12345678]}')
'{"coordinates": [-115.123457, 58.123457], "type": "Point"}'
```

Contributions are welcome on the `geojson` library and on this tartiflette plugin.