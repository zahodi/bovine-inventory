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

    As of right now only hosts and groups types are allowed.
    """
    if (inv_type == 'hosts') or (inv_type == 'groups'):
      result = [i for i in self.inventory[inv_type] if re.search(keyword, i)]
    else:
      # Possibly in future enable search on both types
      result = "Wrong type requested"

    if result == []:
      result = "no results"

    return result

  def vars_list(self, inv_type, keyword):
    """List vars

    List group or host vars
    """
    if (inv_type == 'hosts') or (inv_type == 'groups'):
      if inv_type == 'groups':
        result = self.inventory[inv_type][keyword]['vars']
      else:
        result = self.inventory[inv_type][keyword]
    else:
      # Possibly in future enable search on both types
      result = "Wrong type requested"

    if result == []:
      result = "no results"

    return result

  def children_list(self, inv_type, keyword):
    """List children

    List group children
    """
    result = self.inventory[inv_type][keyword]['children']
    if result == []:
      result = "no results"

    return result
