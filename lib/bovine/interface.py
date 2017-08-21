#!/usr/bin/env python3

from bovine import app
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
      list_of_groups = []
      list_of_hosts = []
      response_info = {
        "status": "success",  # to add failure later
        "data": {
          "groups": list_of_groups,
          "hosts": list_of_hosts
        }
      }
      if keyword in self.inventory['groups']:
        list_of_groups.append(keyword)
      if keyword in self.inventory['hosts']:
        list_of_hosts.append(keyword)

    else:
      pass  # fail because only hosts, groups, or any are allowed in the "types"

    return response_info
