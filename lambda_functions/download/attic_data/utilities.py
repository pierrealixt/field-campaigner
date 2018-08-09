import json
import calendar
import datetime
from aws import S3Data

def format_query(parameters):
    return (
        '('
        '{element_parameters}'
        ');'
        '(._;>;);'
        'out {print_mode};'
    ).format(**parameters)

def serialize_overpass_data(filename):
    overpass_data = S3Data().fetch(
        'data/overpass/{}.json'.format(filename))

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


def cast_date_to_timgm(date):
    return calendar.timegm(datetime.datetime.strptime(
            date, '%Y-%m-%d').timetuple()) * 1000

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

