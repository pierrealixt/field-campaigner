import unittest
import warnings
from lambda_function import (
    lambda_handler
)

class TestCase(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")   

    def test_run(self):
        event = {
           'campaign_uuid': '350f14d1e3c24c7f848a32ff0a552748', 
           'feature': 'building=yes'
        }
        lambda_handler(event, {})


if __name__ == '__main__':
    unittest.main()