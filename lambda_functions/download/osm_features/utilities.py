import json
import requests
import os
import hashlib
import boto3
import json
from shapely import geometry as shapely_geometry
from shapely.ops import cascaded_union
from shapely.geometry.geo import mapping
from aws import S3Data


def multi_feature_to_polygon(geojson):
    """ Convert multi features to be multipolygon
    as single geometry.

    :param geojson: Geojson that
    :type geojson: dict

    :return: Nice geojson with multipolygon
    :rtype:dict
    """
    cascaded_geojson = None
    if len(geojson['features']) > 0:
        polygons = []
        for feature in geojson['features']:
            polygons.append(shapely_geometry.Polygon(
                feature['geometry']['coordinates'][0]
            ))
        cascaded_polygons = cascaded_union(polygons)
        cascaded_geojson = mapping(cascaded_polygons)

        coords_length = len(json.dumps(cascaded_geojson['coordinates']))

        if coords_length > 1000:
            # Simplify the polygons
            simplified_polygons = simplify_polygon(cascaded_polygons, 0.001)
            cascaded_geojson = mapping(simplified_polygons)

    geojson['features'] = [{
        "type": "Feature", "properties": {},
        "geometry": cascaded_geojson
    }]
    return geojson

def save_to_s3(filename, data):
    S3Data().create('data/osm_features/{}.json'.format(filename), data)

def serialize_geometry(geometry):
    single_geometry = multi_feature_to_polygon(geometry)
    return json.dumps(single_geometry['features'][0]['geometry'])


def get_request(geometry, start_date, end_date):
    print(geometry)
    return
    payload = {
        'page': 1,
        'page_size': 15,
        'geometry': geometry,
        'date__gte': start_date,
        'date__lte': end_date,
        'area_lt': 2
    }
    data = requests.get(
        'https://osmcha.mapbox.com/api/v1/features/',
        params=payload,
        timeout=60,
    )
    print(data.url)

    return data.text.encode('utf-8')

def split_polygon(polygon):
    """Split polygon array to string.

    :param polygon: list of array describing polygon area e.g.
    '[[28.01513671875,-25.77516058680343],[28.855590820312504,-25.567220388070023],
    [29.168701171875004,-26.34265280938059]]
    :type polygon: list

    :returns: A string of polygon e.g. 50.7 7.1 50.7 7.12 50.71 7.11
    :rtype: str
    """

    if len(polygon) < 3:
        raise ValueError(
                'At least 3 lat/lon float value pairs must be provided')

    polygon_string = ''

    for poly in polygon:
        polygon_string += ' '.join(map(str, poly))
        polygon_string += ' '

    return polygon_string.strip()

def simplify_polygon(polygon, tolerance):
    """Simplify polygon geometry.

    :param polygon: polygon object to simplified
    :type polygon: Shapely polygon

    :param tolerance: tolerance of simplification
    :type tolerance: float
    """
    simplified_polygons = polygon.simplify(
        tolerance,
        preserve_topology=True
    )
    return simplified_polygons

def parse_json_string(json_string):
    """Parse json string to object, if it fails then return none

    :param json_string: json in string format
    :type json_string: str

    :return: object or none
    :rtype: dict/None
    """
    json_object = None

    if not isinstance(json_string, str):
        return json_string

    try:
        json_object = json.loads(json_string)
    except (ValueError, TypeError):
        pass
    return json_object
