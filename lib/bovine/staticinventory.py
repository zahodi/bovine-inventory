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

  def _get_all_groups(self):
    '''Walk the groups/ dir, saving all found groups

    Then, load all variables, hosts and child groups from each group
    '''
    groups_directory = self.root_directory + '/groups'
    os.listdir(groups_directory)

    pass


  def _get_all_hosts(self):
    '''
    Walk the hosts/ dir, saving all found hosts
    Then, load all variables from each host
    '''

    pass

  def calc_meta_info(self):
    '''
    Calculate the meta information about groups and hosts.
    i.e. build the tree of groups, sub groups etc.
    '''

    pass

  def get_file_names(self, root_directory):
    '''
    NB: This method to be deprecated
    Walks directory to get all files as a list
    '''
    directory_files = os.walk(root_directory)
    file_names = []

    for root, dirs, files in directory_files:
      for name in files:
        file_names.append(os.path.join(root, name))

    return file_names


  # import the yaml from the files that we found above
  def import_yaml(self):
    '''
    NB: This method to be deprecated
    Loads yaml from found files and converts to native python objects
    '''

    load_of_yaml = []

    file_names = self.get_file_names(self.root_directory)

    for name in file_names:
      with open(name, 'r') as f:
        load_of_yaml = yaml.load(f)

    return load_of_yaml


  def get_inventory(self):
    '''
    NB: This method to be deprecated
    '''

    self.load_of_yaml = self.import_yaml()


  def print_inventory(self):
    '''
    NB: This method to be deprecated
    '''

    return self.load_of_yaml
