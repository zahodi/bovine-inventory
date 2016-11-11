#!/usr/bin/env python3
import os
import yaml
##########################
# Read the Static Directory
##########################


class Inventory:
  def __init__(self, root_directory):
    # get the files in the root_directory
    # self.
    self.root_directory = root_directory
    # import the yaml from the files that we found above
  def get_file_names(self, root_directory):
    directory_files = os.walk(root_directory)
    filenames = []
    for root, dirs, files in directory_files:
      for name in files:
        filenames.append(os.path.join(root, name))
    return filenames
    # print(filenames)


  def import_yaml(self):
    load_of_yaml = []
    self.filenames = self.get_file_names(self.root_directory)
    for name in self.filenames:
      with open(name, 'r') as f:
        load_of_yaml = yaml.load(f)
    return load_of_yaml
    self.load_of_yaml = load_of_yaml

  def get_inventory(self):
    self.inventory = self.import_yaml()
    return self.inventory

test_inventory = Inventory('../test/test_data')
print(yaml.dump(test_inventory.get_inventory()))
