#!/usr/bin/env python3
import os
import yaml
##########################
# Read the Static Directory
##########################


class Inventory:
  def __init__(self, root_directory):
    # get the files in the root_directory
    self.root_directory = root_directory

  def get_file_names(self, root_directory):
    directory_files = os.walk(root_directory)
    file_names = []

    for root, dirs, files in directory_files:
      for name in files:
        file_names.append(os.path.join(root, name))

    return file_names


  # import the yaml from the files that we found above
  def import_yaml(self):
    load_of_yaml = []

    file_names = self.get_file_names(self.root_directory)

    for name in file_names:
      with open(name, 'r') as f:
        load_of_yaml = yaml.load(f)

    return load_of_yaml

  def get_inventory(self):
    self.load_of_yaml = self.import_yaml()

  def print_inventory(self):
    return self.load_of_yaml

test_inventory = Inventory('../test/test_data')
test_inventory.get_inventory()

print(
  yaml.dump(
    test_inventory.print_inventory()
  )
)
