#!/usr/bin/env python3
import os
import yaml
##########################
# Read the Static Directory
##########################
def list_of_files(root_directory):
  directory_files = os.walk(root_directory)
  filenames = []
  for root, dirs, files in directory_files:
    for name in files:
      filenames.append(os.path.join(root, name))
  return filenames
  # print(filenames)


def import_yaml(filenames):
  for name in filenames:
    with open(name, 'r') as f:
      print(yaml.load(f))

import_yaml(list_of_files('../test/test_data'))
