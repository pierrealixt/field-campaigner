import json


def feature_to_filename(feature):
    return '{key}{op}{values}'.format(
        key=feature['key'],
        op='=' if len(feature['values']) > 0 else '',
        values=','.join(feature['values']))
    # if len(feature['values']) == 0:
    #     return '{key}'.format(key=feature['key'])
    # return '{key}={values}'.format(
    #     key=feature['key'],
    #     values=','.join(feature['values']))

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

