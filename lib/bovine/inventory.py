#!/usr/bin/env python3
import os
import yaml

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
      "_group_tree": {},
      "groups": {},
      "hosts": {
      }
    }

    self._get_all_groups()
    self._get_all_hosts()
    self.calc_meta_info()

  def debug_print(self):
    print(self.inventory)

  def _get_all_groups(self):
    '''Walk the groups/ dir, saving all found groups

    Then, load all variables, hosts and child groups from each group
    '''
    groups_directory = self.root_directory + 'groups/'
    list_of_groups = os.listdir(groups_directory)
    group_dict = {"groups": {}}
    for filename in list_of_groups:
      if filename.lower().endswith(('.yml', '.yaml')):
        with open(groups_directory + filename, 'r') as stream:
          try:
            group_dict = yaml.safe_load(stream)
            self._merge_dicts(self.inventory['groups'], group_dict)

          except yaml.YAMLError as exc:
            print(exc)
      else:
        pass

  def _get_all_hosts(self):
    '''
    Walk the hosts/ dir, saving all found hosts
    Then, load all variables from each host
    '''
    hosts_directory = self.root_directory + '/hosts'
    list_of_hosts = os.listdir(hosts_directory)
    host_dic = {"hostvars": {}}
    for i in list_of_hosts:
      if i.lower().endswith(('.yml', '.yml')):
        with open(hosts_directory + '/' + i, 'r') as stream:
          try:
            host_dic = yaml.safe_load(stream)
            self._merge_dicts(self.inventory['_meta']['hostvars'], host_dic)
          except yaml.YAMLError as exc:
            print(exc)
      else:
        pass

  def _parse_yaml(self, yml_obj):
    '''
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

  def calc_meta_info(self):
    '''
    Calculate the meta information about groups and hosts.
    i.e. build the tree of groups, sub groups etc.

    This method probably doesn't make sense any more.
    It will likely be deprecated shortly.
    '''

    pass
