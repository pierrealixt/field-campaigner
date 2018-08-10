import json
import requests
import os
import hashlib
import boto3
import json
from aws import S3Data

def build_payload(uuid, filename, date):
    return json.dumps({
        'campaign_uuid': uuid,
        'filename': filename,
        'date': date
    })

def download_attic_data(payload):
    aws_lambda = boto3.client('lambda')
    aws_lambda.invoke(
        FunctionName='download_attic_data',
        InvocationType='Event',
        Payload=payload)    

def format_query(parameters):
    if parameters['value']:
        query = template_query_with_value()
    else:
        query = template_query()

    return query.format(**parameters)

def format_feature_values(feature_values):
    return '|'.join(feature_values)

def build_query(polygon, feature):
    parameters = {
        'polygon': split_polygon(polygon),
        'print_mode': 'meta',
        'key': feature['key'],
        'value': format_feature_values(feature['values'])
    }
    return format_query(parameters)

def template_query():
    return ('[out:json];('
        'way["{key}"]'
        '(poly:"{polygon}");'
        'node["{key}"]'
        '(poly:"{polygon}");'
        'relation["{key}"]'
        '(poly:"{polygon}");'
        ');'
        '(._;>;);'
        'out {print_mode};')

def template_query_with_value():
    return ('[out:json];('
        'way["{key}"~"{value}"]'
        '(poly:"{polygon}");'
        'node["{key}"~"{value}"]'
        '(poly:"{polygon}");'
        'relation["{key}"~"{value}"]'
        '(poly:"{polygon}");'
        ');'
        '(._;>;);'
        'out {print_mode};')

def post_request(query):
    data = requests.post(
        url='http://exports-prod.hotosm.org:6080/api/interpreter',
        data={'data': query},
        headers={'User-Agent': 'HotOSM'})

    return data.text.encode('utf-8')

def save_to_s3(filename, data):
    S3Data().create('data/overpass/{}.json'.format(filename), data)

def date_to_dict(start_date, end_date):
    return {
        'from': start_date,
        'to': end_date
    }

def feature_to_filename(feature):
    return '{key}{op}{values}'.format(
        key=feature['key'],
        op='=' if len(feature['values']) > 0 else '',
        values=','.join(feature['values']))

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
