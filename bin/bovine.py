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

    self.file_names = file_names


  # import the yaml from the files that we found above
  def import_yaml(self):
    load_of_yaml = []

    self.get_file_names(self.root_directory)

    for name in self.file_names:
      with open(name, 'r') as f:
        load_of_yaml = yaml.load(f)

    self.load_of_yaml = load_of_yaml

  def get_inventory(self):
    self.import_yaml()
    return self.load_of_yaml #defined in import_yaml method

test_inventory = Inventory('../test/test_data')

print(
  yaml.dump(
    test_inventory.get_inventory()
  )
)
