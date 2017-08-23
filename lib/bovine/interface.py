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

    This will return the whole inventory:

    Return
    ------
    {
      "hosts": {
        "host1":
          "var1": "value1"
        }
      }
      "groups": {
        "group1": {
          "vars": {
            "var1": "value1"
          },
          "children": [
            "group2"
          ],
          "children": [
            "group2"
          ]
          "hosts": [
              "host1"
          ]
        }
      }
      "top_level_groups": {
          "group1": {},
          "group6": {}
      }
    }
    """
    test_inventory = StaticInventory(root_directory='test/test_data/static/')
    return test_inventory.inventory

  def search(self, inv_type, keyword):
    """Search the inventory

    Search the inventory for hosts or group. As of right now only hosts and
    groups types are allowed.

    Parameters
    ----------
    inv_type: str
      Type of inventory to look for. Hosts or groups
    keyword: str
      Lookup name

    Returns
    ----------
    [
      "host1",
      "host2"
    ]
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

    List group or host vars.

    Parameters
    ----------
    inv_type: str
      Type of inventory to look for. Hosts or groups
    keyword: str
      host or group name

    Returns
    ----------
    {
      "var1": "value1"
    }
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

  def children_list(self, keyword):
    """List children

    List children of a specified group

    Parameters
    ----------
    keyword: str
      group name

    Returns
    ----------
    [
      "group1",
      "group2"
    ]
    """
    result = self.inventory['groups'][keyword]['children']
    if result == []:
      result = "no results"

    return result
