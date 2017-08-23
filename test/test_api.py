import sys
import unittest
from unittest import TestCase
sys.path.append('lib/')
from bovine import api
import json



class TestIntegrations(TestCase):
  def setUp(self):
    self.app = api.test_client()

  def test_thing(self):
    response = self.app.get('api/')
    payload = json.loads(response.get_data(response))
    self.assertEqual(payload, {'hello': 'world'})

if __name__ == "__main__":
    unittest.main()
