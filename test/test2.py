#!/usr/bin/env python3

import sys
sys.path.append('./lib/')

from bovine.staticinventory import *

i = StaticInventory(root_directory='./test/test_data/static/')
