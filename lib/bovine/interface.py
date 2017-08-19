#!/usr/bin/env python3

from bovine import bovine
from bovine.inventory import *
import json


class Interface(object):
  """Modify inventory

  Interface class to search, add, modify, and delete hosts or groups
  in the static inventory
  """
  def __init__(self):
    self.inventory = self.get_all()

  def get_all(self):
    test_inventory = StaticInventory(root_directory='../test/test_data/static/')
    return test_inventory.inventory

  def search(self, hostname):
    return self.inventory['hosts'][hostname]
