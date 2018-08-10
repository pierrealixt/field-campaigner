import unittest
from lambda_function import fetch_attributes


class TestCase(unittest.TestCase):
  def test_fetch_attributes(self):
    feature = 'amenity=cafe'
    function_name = 'FeatureAttributeCompleteness'
    functions = {
        "function-1": {
            "function": "FeatureAttributeCompleteness", 
            "feature": "amenity=cafe", 
            "attributes": {"amenity": ["cafe"], "name": [], "cuisine": [], "operator": [], "opening_hours": []}, 
            "type": "cafe"}, 
        "function-2": {
            "function": "CountFeature", "feature": "amenity=cafe", 
            "attributes": {"amenity": ["cafe"], "name": [], "cuisine": [], "operator": [], "opening_hours": []},
            "type": "cafe"}, 
        "function-3": {
            "function": "MapperEngagement", "feature": "amenity=cafe", 
            "attributes": {"amenity": ["cafe"], "name": [], "cuisine": [], "operator": [], "opening_hours": []}, 
            "type": "cafe"}, 
        "function-4": {
            "function": "FeatureAttributeCompleteness", "feature": "shop=supermarket", 
            "attributes": {"shop": ["supermarket"], "name": []}, 
            "type": "supermarket"}, 
        "function-5": {
            "function": "CountFeature", "feature": "shop=supermarket", 
            "attributes": {"shop": ["supermarket"], "name": []},
            "type": "supermarket"}, 
        "function-6": {
            "function": "MapperEngagement", 
            "feature": "shop=supermarket", 
            "attributes": {"shop": ["supermarket"], "name": []}, 
            "type": "supermarket"}
        }
    attributes = fetch_attributes(feature, function_name, functions)
    self.assertEqual(attributes, {"amenity": ["cafe"], "name": [], "cuisine": [], "operator": [], "opening_hours": []})

if __name__ == '__main__':
  unittest.main()