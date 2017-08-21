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
    """Return the whole inventory

    We will get the whole inventory
    """
    test_inventory = StaticInventory(root_directory='../test/test_data/static/')
    return test_inventory.inventory

  def search(self, inv_type, keyword):
    """Search the inventory

    Any, hosts, and groups types are allowed.
    """
    if (inv_type == 'hosts') or (inv_type == 'groups'):
      return self.inventory[inv_type][keyword]
    elif inv_type == 'any':
      response_info = {
        "status": "success",  # to add failure later
        "data": {
          "groups": [],
          "hosts": []
        }
      }
      for i in self.inventory:
        return i
        if keyword in i:
          pass

    else:
      pass  # fail because only hosts, groups, or any are allowed in the "types"
