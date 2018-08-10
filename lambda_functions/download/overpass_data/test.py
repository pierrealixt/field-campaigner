import warnings
import unittest
from lambda_function import (
    lambda_handler
)

from utilities import (
    feature_to_filename,
    date_to_dict,
    format_query,
    format_feature_values
)

class TestCase(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings(
            "ignore", 
            category=ResourceWarning, 
            message="unclosed.*<ssl.SSLSocket.*>") 

    def test_run(self):
        event = {
            'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893',
            'feature': {
                'key': 'amenity',
                'values': ['cafe']
            }
        }
        lambda_handler(event, {})

    def test_feature_to_filename_1(self):
        feature = {
            'key': 'amenity',
            'values': ['cafe']
        }
        filename = feature_to_filename(feature)
        self.assertEqual(filename, 'amenity=cafe')

    def test_feature_to_filename_2(self):
        feature = {
            'key': 'amenity',
            'values': []
        }
        filename = feature_to_filename(feature)
        self.assertEqual(filename, 'amenity')

    def test_feature_to_filename_3(self):
        feature = {
            'key': 'amenity',
            'values': ['cafe', 'coffee']
        }
        filename = feature_to_filename(feature)
        self.assertEqual(filename, 'amenity=cafe,coffee')

    def test_date_to_dict(self):
        start_date = '2018-08-01'
        end_date = '2018-08-31'
        date = date_to_dict(start_date, end_date)
        self.assertEqual(date, {'from': '2018-08-01', 'to': '2018-08-31'})

    def test_format_query_no_value(self):
        formatted_value = format_feature_values([])
        parameters = {
            'polygon': 'polypolygon',
            'print_mode': 'meta',
            'key': 'amenity',
            'value': formatted_value
        }
        query = format_query(parameters) 
        self.assertEqual(query, '[out:json];(way["amenity"](poly:"polypolygon");node["amenity"](poly:"polypolygon");relation["amenity"](poly:"polypolygon"););(._;>;);out meta;')

    def test_format_query_with_value(self):
        formatted_value = format_feature_values(['cafe'])
        parameters = {
            'polygon': 'polypolygon',
            'print_mode': 'meta',
            'key': 'amenity',
            'value': formatted_value
        }
        query = format_query(parameters)
        self.assertEqual(query, '[out:json];(way["amenity"~"cafe"](poly:"polypolygon");node["amenity"~"cafe"](poly:"polypolygon");relation["amenity"~"cafe"](poly:"polypolygon"););(._;>;);out meta;')

    def test_format_query_with_values(self):
        formatted_value = format_feature_values(['cafe', 'coffee'])
        parameters = {
            'polygon': 'polypolygon',
            'print_mode': 'meta',
            'key': 'amenity',
            'value': formatted_value
        }
        query = format_query(parameters)
        self.assertEqual(query, '[out:json];(way["amenity"~"cafe|coffee"](poly:"polypolygon");node["amenity"~"cafe|coffee"](poly:"polypolygon");relation["amenity"~"cafe|coffee"](poly:"polypolygon"););(._;>;);out meta;')

if __name__ == '__main__':
    unittest.main()

