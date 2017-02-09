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
            
            #--------------------------------
            ## merge data into group_dict
            ## this ONLY works on python 3.5+
            ## this does NOT take into account the complexities
            ##   of the data though (i.e. it's only a shallow merge)
            ## this will be moved into the _parse_yaml() method,
            ##   and will need to be expanded to deep deep dict merging.
            #--------------------------------
            group_dict = {**group_dict, **fresh_dict}

            #TODO: uncomment below (and remove above) once _merge_dicts working
            #TODO: verify that passing these params by reference is not munging our data
            # group_dict = _merge_dicts(group_dict,temp_dict) 

            #--------------------------------
            # delete below
            #--------------------------------
            print(group_dict)

          except yaml.YAMLError as exc:
            print(exc)
      else:
        pass

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

  def _parse_yaml(self,yml_obj):
    '''
    Take in data loaded from a yml file, 
    and parse it for groups, hosts and vars.
    '''

  def _merge_dicts(self, dict1, dict2):
    '''
    Takes in two dicts of arbitrary nested levels, 
    and intelligently merges them (i.e. deep dict merge)
    '''

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
