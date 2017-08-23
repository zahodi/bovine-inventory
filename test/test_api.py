#!/usr/bin/env python3
import json
import sys
import unittest
from unittest import TestCase
sys.path.append('lib/')
from bovine import api


class TestIntegrations(TestCase):
  def setUp(self):
    self.app = api.test_client()

  def test_thing(self):
    response = self.app.get('api/')
    payload = json.loads(response.get_data(response))
    self.assertEqual(payload, {'hello': 'world'})

  def test_list_groups_vars(self):
    response = self.app.post('api/vars?action=list&name=group1&type=groups')
    payload = json.loads(response.get_data(response))
    print("group1 vars are: ", payload)
    self.assertEqual(payload, {'foo': 'bar'})

  def test_list_hosts_vars(self):
    response = self.app.post('api/vars?action=list&name=host1&type=hosts')
    payload = json.loads(response.get_data(response))
    print("host1 vars are: ", payload)
    self.assertEqual(payload, {'foo': 'bar1'})

  def test_list_children(self):
    response = self.app.post('api/children?action=list&name=group1')
    payload = json.loads(response.get_data(response))
    print("group1 children are: ", payload)
    self.assertEqual(payload, ["group2", "group3", "group4"])

if __name__ == "__main__":
    unittest.main()
