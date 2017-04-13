#!/usr/bin/env python3
import unittest
import sys
import json
# import os
# from .context import bovine

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('lib/')
from bovine.inventory import *


class TestStringMethods(unittest.TestCase):

    #################
    # sanity tests
    #################

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


class TestStaticInventory(unittest.TestCase):
    ####################################
    # Test bovine.StaticInventory module
    #####################################
    def setUp(self):
        self.test_inventory = StaticInventory(root_directory='test/test_data/static/')

    def test_static_inventory(self):
        self.assertIsInstance(self.test_inventory, StaticInventory)
        print(
            json.dumps(
                self.test_inventory.inventory,
                indent=4
            )
        )

    def test_keys_present(self):
        self.assertTrue("groups" in self.test_inventory.inventory)
        self.assertTrue("hosts" in self.test_inventory.inventory)
        self.assertTrue("top_level_groups" in self.test_inventory.inventory)
        self.assertTrue("child_groups" in self.test_inventory.inventory)

    def test_hosts_key(self):
        hosts_should_have = {
            "host1": { "foo": "bar1" },
            "host2": { "foo": "bar2" },
            "host3": { "foo": "bar3" },
            "host4": { "foo": "bar4" },
            "host5": { "foo": "bar5" },
            "host6": { "foo": "bar6" },
        }
        self.assertCountEqual(hosts_should_have, self.test_inventory.inventory['hosts'])

    def test_top_level_groups(self):
        top_level_groups_should_have = {
            "group1": {},
            "group6": {},
        }
        self.assertCountEqual(top_level_groups_should_have, self.test_inventory.inventory['top_level_groups'])

if __name__ == '__main__':
    unittest.main()
