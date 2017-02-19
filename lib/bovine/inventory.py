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
        "hosts":  {},
        "groups": {},
        "_meta":  {},
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
            temp_dict = yaml.safe_load(stream)

            #TODO: uncomment below (and remove above) once _merge_dicts working
            #TODO: verify that passing these params by reference is not munging our data
            group_dict = self._merge_dicts(group_dict, temp_dict)


          except yaml.YAMLError as exc:
            print(exc)
      else:
        pass

    print(group_dict)
    return group_dict #we won't want to return, but actually merge with the self.inventory


  def _get_all_hosts(self):
    '''
    Walk the hosts/ dir, saving all found hosts
    Then, load all variables from each host
    '''
    hosts_directory = self.root_directory + '/hosts'
    list_of_hosts = os.listdir(hosts_directory)
    host_dic = {}
    for i in list_of_hosts:
      if i.lower().endswith(('.yml', '.yml')):
        with open(hosts_directory + '/' + i, 'r') as stream:
          try:
            host_dic = yaml.safe_load(stream)
            return host_dic
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

    # ## debug output
    # sys.stderr.write("DEBUG: %s to %s\n" %(b,a))

    try:
      if ( a is None or isinstance(a, str)
           or isinstance(a, unicode)
           or isinstance(a, int)
           or isinstance(a, long)
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
              a[key] = data_merge(a[key], b[key])
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

#  def get_file_names(self, root_directory):
#    '''
#    NB: This method to be deprecated
#    Walks directory to get all files as a list
#    '''
#    directory_files = os.walk(root_directory)
#    file_names = []
#
#    for root, dirs, files in directory_files:
#      for name in files:
#        file_names.append(os.path.join(root, name))
#
#    return file_names
#
#
#  # import the yaml from the files that we found above
#  def import_yaml(self):
#    '''
#    NB: This method to be deprecated
#    Loads yaml from found files and converts to native python objects
#    '''
#
#    load_of_yaml = []
#
#    file_names = self.get_file_names(self.root_directory)
#
#    for name in file_names:
#      with open(name, 'r') as f:
#        load_of_yaml = yaml.load(f)
#
#    return load_of_yaml
#
#
#  def get_inventory(self):
#    '''
#    NB: This method to be deprecated
#    '''
#
#    self.load_of_yaml = self.import_yaml()
#
#
#  def print_inventory(self):
#    '''
#    NB: This method to be deprecated
#    '''
#
#    return self.load_of_yaml
