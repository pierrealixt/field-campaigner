import os
import json
import boto3
import requests
import calendar
import datetime
from aws import S3Data


def build_payload(uuid, feature, date):
    return json.dumps({
        'campaign_uuid': uuid,
        'feature': feature,
        'date': date
    })


def invoke_download_attic_data(payload):
    aws_lambda = boto3.client('lambda')
    function_name_with_env = '{env}_download_attic_data'.format(
        env=os.environ['ENV'])

    aws_lambda.invoke(
        FunctionName=function_name_with_env,
        InvocationType='Event',
        Payload=payload)


def format_overpass_query(parameters):
    if parameters['value']:
        query = template_query_with_value()
    else:
        query = template_query()

    return query.format(**parameters)


def format_feature_values(feature_values):
    return '|'.join(feature_values)


def build_overpass_query(polygon, feature):
    key, values = split_feature_key_values(feature)
    parameters = {
        'polygon': split_polygon(polygon),
        'print_mode': 'meta',
        'key': key,
        'value': format_feature_values(values)
    }
    return format_overpass_query(parameters)

def build_overpass_path(uuid, feature):
    return '/'.join([
        'campaigns/{uuid}',
        'raw_data/overpass/{feature}.json'
        ]).format(
            uuid=uuid,
            feature=feature)


def build_attic_path(uuid, feature):
    return '/'.join([
        'campaigns/{uuid}',
        'raw_data/attic',
        '{feature}.xml']).format(
            uuid=uuid,
            feature=feature)


def template_query():
    return (
        '[out:json];('
        'way["{key}"]'
        '(poly:"{polygon}");'
        'node["{key}"]'
        '(poly:"{polygon}");'
        'relation["{key}"]'
        '(poly:"{polygon}");'
        ');'
        '(._;>;);'
        'out {print_mode};'
    )


def template_query_with_value():
    return (
        '[out:json];('
        'way["{key}"~"{value}"]'
        '(poly:"{polygon}");'
        'node["{key}"~"{value}"]'
        '(poly:"{polygon}");'
        'relation["{key}"~"{value}"]'
        '(poly:"{polygon}");'
        ');'
        '(._;>;);'
        'out {print_mode};'
    )


def post_request(query):
    print('posting request...')
    data = requests.post(
        url='http://exports-prod.hotosm.org:6080/api/interpreter',
        data={'data': query},
        headers={'User-Agent': 'HotOSM'})
    print('done posting.')
    return data.text.encode('utf-8')


def save_to_s3(path, data):
    print('saving to s3...')
    S3Data().create(path, data)
    print('done saving.')


def date_to_dict(start_date, end_date):
    return {
        'from': start_date,
        'to': end_date
    }


def cast_element_ids_to_s(hash_element_ids):
    """
    Cast a hash of element ids to a string of element ids.
    :param hash_element_ids: node/relation/way ids
    :type hash_element_ids: hash
    :returns: a string of node/relation/way ids
    :rtype: str
    """
    elements_to_s = str()
    for el in ['node', 'relation', 'way']:
        if len(hash_element_ids[el]) > 0:
            el_to_s = '{}(id:{});'.format(
                el,
                ','.join(str(element)
                         for element in hash_element_ids[el]))
            elements_to_s += el_to_s
    return elements_to_s


def serialize_overpass_data(uuid, feature):
    path = 'campaigns/{uuid}/raw_data/overpass/{feature}.json'.format(
        uuid=uuid,
        feature=feature)

    overpass_data = S3Data().fetch(path)

    elements_ids = {
        'node': [],
        'way': [],
        'relation': []
    }
    for element in overpass_data['elements']:
        try:
            elements_ids[element['type']].append(str(element['id']))
        except ValueError:
            pass
    return elements_ids


def build_attic_query(uuid, feature):
    elements_ids = serialize_overpass_data(uuid, feature)

    parameters = {
        'element_parameters': cast_element_ids_to_s(elements_ids),
        'print_mode': 'meta'
    }
    return format_attic_query(parameters)


def cast_date_to_timgm(date):
    return calendar.timegm(datetime.datetime.strptime(
            date, '%Y-%m-%d').timetuple()) * 1000


def build_diff_attic_query(date):
    date_from = cast_date_to_timgm(date['from'])
    date_to = cast_date_to_timgm(date['to'])

    datetime_from = datetime.datetime.utcfromtimestamp(
            float(date_from) / 1000.)
    datetime_to = datetime.datetime.utcfromtimestamp(
            float(date_to) / 1000.)
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    diff_query = '[diff:"{date_from}", "{date_to}"];'.format(
            date_from=datetime_from.strftime(date_format),
            date_to=datetime_to.strftime(date_format)
    )
    return diff_query


def format_attic_query(parameters):
    return (
        '('
        '{element_parameters}'
        ');'
        '(._;>;);'
        'out {print_mode};'
    ).format(**parameters)


def feature_to_filename(feature):
    return '{key}{op}{values}'.format(
        key=feature['key'],
        op='=' if len(feature['values']) > 0 else '',
        values=','.join(feature['values']))

def split_feature_key_values(feature):
    if '=' not in feature:
        feature = '{}='.format(feature)
    key, values = feature.split('=')
    if len(values) == 0:
        values = []
    else:
        values = values.split(',')
    return key, values


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