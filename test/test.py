#!/usr/bin/env python3
import unittest
import sys
# import os
# from .context import bovine

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('lib/')
from bovine import staticinventory


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
    def test_static_inventory(self):
        test_inventory = staticinventory.StaticInventory('test_data')
        self.assertIsInstance(test_inventory, staticinventory.StaticInventory)

if __name__ == '__main__':
    unittest.main()
