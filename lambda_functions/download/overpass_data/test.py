import unittest
from utilities import (
    feature_to_filename
)

class TestCase(unittest.TestCase):
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

if __name__ == '__main__':
  unittest.main()

