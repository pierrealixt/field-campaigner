import json
import os

def get_unique_features(functions):
    features = []
    for function in functions:
        features.append(functions[function]['feature'])
    return set(features)

def split_feature_key_values(feature):
    key, values = feature.split('=')
    if len(values) == 0:
        values = None
    else:
        values = values.split(',')
    return key, values


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

