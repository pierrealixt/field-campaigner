import unittest
from lambda_function import lambda_handler
from utilities import (
  get_unique_features,
  split_feature_key_values
)

class TestCase(unittest.TestCase):

    def test_run(self):
      event = {'campaign_uuid': 'cabbf57b1ac3410cafdd6d64abb1c893'}
      lambda_handler(event, {})

    def test_get_unique_features(self):
        selected_functions = {
          "function-1": {"function": "FeatureAttributeCompleteness", "feature": "amenity=cafe", "attributes": {"amenity": ["cafe"], "name": [], "cuisine": [], "operator": [], "opening_hours": []}, "type": "cafe"}, 
          "function-2": {"function": "CountFeature", "feature": "amenity=cafe", "attributes": {"amenity": ["cafe"], "name": [], "cuisine": [], "operator": [], "opening_hours": []}, "type": "cafe"},
          "function-3": {"function": "MapperEngagement", "feature": "amenity=cafe", "attributes": {"amenity": ["cafe"], "name": [], "cuisine": [], "operator": [], "opening_hours": []}, "type": "cafe"},
          "function-4": {"function": "FeatureAttributeCompleteness", "feature": "shop=supermarket", "attributes": {"shop": ["supermarket"], "name": []}, "type": "supermarket"},
          "function-5": {"function": "CountFeature", "feature": "shop=supermarket", "attributes": {"shop": ["supermarket"], "name": []}, "type": "supermarket"},
          "function-6": {"function": "MapperEngagement", "feature": "shop=supermarket", "attributes": {"shop": ["supermarket"], "name": []}, "type": "supermarket"}
        }

        unique_features = get_unique_features(selected_functions)

        self.assertEqual(unique_features, {'amenity=cafe', 'shop=supermarket'})

    def test_split_feature_key_values_1(self):
      feature = 'amenity=cafe'
      key, values = split_feature_key_values(feature)
      self.assertEqual(key, 'amenity')
      self.assertEqual(values, ['cafe'])

    def test_split_feature_key_values_2(self):
      feature = 'landuse='
      key, values = split_feature_key_values(feature)
      self.assertEqual(key, 'landuse')
      self.assertEqual(values, None)

    def test_split_feature_key_values_3(self):
      feature = 'amenity=cafe,coffee'
      key, values = split_feature_key_values(feature)
      self.assertEqual(key, 'amenity')
      self.assertEqual(values, ['cafe', 'coffee'])

    def test_filename_1(self):
      feature = 'amenity=cafe'
      

if __name__ == '__main__':
    unittest.main()