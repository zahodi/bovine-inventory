#!/usr/bin/env python3
from bovine.inventory import StaticInventory
import re


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
    test_inventory = StaticInventory(root_directory='test/test_data/static/')
    return test_inventory.inventory

  def search(self, inv_type, keyword):
    """Search the inventory

    Any, hosts, and groups types are allowed.
    """
    if (inv_type == 'hosts') or (inv_type == 'groups'):
      result = [i for i in self.inventory[inv_type] if re.search(keyword, i)]
    else:
      result = "no results"

    return result

  def re_filter(self, pattern, string):
     return re.match(pattern, string)
