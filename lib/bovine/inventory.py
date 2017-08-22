#!/usr/bin/env python3
import os
import yaml
# import sys


class StaticInventory:
  def __init__(self, root_directory=None):
    '''Init instance

    Optional args:
      # the root directory to find the hosts/ and groups/ directories
      - root_directory='foo'
    '''

    # root_directory
    if root_directory is None:
      root_directory = './static/'
    self.root_directory = root_directory

    # hosts and groups
    self.inventory = {
      "groups": {},
      "hosts": {},
      "top_level_groups": {},
      "child_groups": {}, # each child group contains a key "parent_groups"
    }

    self._get_all_groups()
    self._get_all_hosts()
    self._calc_group_tree()

  def debug_print(self):
    print(
        json.dumps(
            self.inventory,
            indent=4,
        )
    )

  def _get_all_groups(self):
    '''Walk the groups/ dir, saving all found groups

    Then, load all variables, hosts and child groups from each group
    '''

    # initialize vars
    group_dict = {"groups": {}}
    groups_directory = self.root_directory + 'groups/'

    # get list of all files in the ./groups/ dir
    # NB: we do NOT recurse, as we expect that all
    #     yaml files will be at the top level
    list_of_groups = os.listdir(groups_directory)

    for filename in list_of_groups:
      if filename.lower().endswith(('.yml', '.yaml')): #ignore non yaml files
        with open(groups_directory + filename, 'r') as stream:
          try:
            group_dict = yaml.safe_load(stream)
            # TODO: check that we have the proper structure?
            #       i.e. vars: {}, children: [], hosts: []
            self._merge_dicts(self.inventory['groups'], group_dict)

          except yaml.YAMLError as exc:
            print(exc)
      else:
        pass

  def _get_all_hosts(self):
    '''Get all hosts

    Walk the hosts/ dir, saving all found hosts
    Then, load all variables from each host
    '''
    hosts_directory = self.root_directory + 'hosts/'
    list_of_hosts = os.listdir(hosts_directory)
    temp_hosts = {"hosts": {} }
    for i in list_of_hosts:
      if i.lower().endswith(('.yml', '.yml')):
        with open(hosts_directory + '/' + i, 'r') as stream:
          try:
            host_dict = yaml.safe_load(stream)
            for temp_host in host_dict['all']['hosts']:
                temp_hosts['hosts'][temp_host] = host_dict['all']['hosts'][temp_host]
            self._merge_dicts(self.inventory, temp_hosts)
          except yaml.YAMLError as exc:
            print(exc)
      else:
        pass

  def _parse_yaml(self, yml_obj):
    '''parse yaml

    Take in data loaded from a yml file,
    and parse it for groups, hosts and vars.
    '''

  def _merge_dicts(self, a, b):
    '''Takes in two dicts of arbitrary nested levels,
    and intelligently merges them (i.e. deep dict merge)

    merges b into a and returns merged result
    NOTE: tuples and arbitrary objects are not handled
          as it is totally ambiguous what should happen
    '''

    key = None
      # or isinstance(a, unicode)
    try:
      if (a is None or isinstance(a, str)
           or isinstance(a, int)
           or isinstance(a, float)
         ):
        # border case for first run or if a is a primitive
        a = b
      elif isinstance(a, list):
        # lists can be only appended
        if isinstance(b, list):
          # merge lists
          #a.extend(b)
          #a.extend(b)
          for item in b:
            if item not in a:
              #a.extend(item)
              a.append(item)
        else:
          # append to list
            a.append(b)
      elif isinstance(a, dict):
        # dicts must be merged
        if isinstance(b, dict):
          for key in b:
            if key in a:
              a[key] = self._merge_dicts(a[key], b[key])
            else:
              a[key] = b[key]
        else:
          raise YamlReaderError('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
      else:
        raise YamlReaderError('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
    except TypeError as e:
      raise YamlReaderError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
    return a

  def _calc_group_tree(self):
    '''
    Calculate the group tree for all hosts and groups.

    This function does 3 things:
      - determine which groups are "top_level_groups"
      - determine which groups are not, assigning them to "child_groups"
      - within child_groups, assign a var "parent_groups" to each group for later lookup

    By having this additional info (i.e. which groups are top_level_groups, and a lookup table
      to determine the parent_groups of all non top_level_groups, we can easily build a graph showing
      the relationship for any group or host, all the way back to its top level group.
    '''

    # ORDER OF LOGIC
    #   loop through all groups:
    #       if this group NOT already in child_groups
    #       AND
    #       if this group NOT already in top_level_groups:
    #           add to top_level_groups list
    #
    #       if group contains "children" key:
    #           for child in children:
    #               if child in top_level_groups:
    #                   remove it
    #               if child NOT in child_groups:
    #                   add it
    #               if group NOT in child['parent_groups']:
    #                   add it

    for group in self.inventory['groups']:
        # if this group NOT already in child_groups
        # AND
        # if this group NOT already in top_level_groups:
        if (
            group not in self.inventory['child_groups']
            and
            group not in self.inventory['top_level_groups']
        ):
            # add to top_level_groups list
            self.inventory['top_level_groups'][group] = {}

        # if group contains "children" key:
        if "children" in self.inventory['groups'][group]:
            for child in self.inventory['groups'][group]['children']:
                # if child in top_level_groups:
                if child in self.inventory['top_level_groups']:
                    # remove it
                    self.inventory['top_level_groups'].pop(child)

                # if child NOT in child_groups:
                if child not in self.inventory['child_groups']:
                    # add it
                    self.inventory['child_groups'][child] = { 'parent_groups': {} }
                # if group NOT in child['parent_groups']:
                if group not in self.inventory['child_groups'][child]['parent_groups']:
                    # add it
                    self.inventory['child_groups'][child]['parent_groups'][group] = {}
