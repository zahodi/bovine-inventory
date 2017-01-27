#!/usr/bin/env python3

import sys
sys.path.append('./lib/')

### TODO: we seriously need to work on namespacing
from bovine.inventory import * 

i = StaticInventory(root_directory='./test/test_data/static/')
