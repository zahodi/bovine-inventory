import sys
import unittest
import requests
sys.path.append('lib/')
import api


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get('http://localhost:5000')
        self.assertEqual(response.json(), {'hello': 'world'})


class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    def test_hello_world(self):
        response = self.app.get('/')

if __name__ == "__main__":
    unittest.main()
