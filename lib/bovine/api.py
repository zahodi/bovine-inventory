from bovine import bovine
from bovine.inventory import *
import json

@bovine.route('/')
def setUp():
    test_inventory = StaticInventory(root_directory='../test/test_data/static/')
    return json.dumps(test_inventory.inventory,
    indent=4)
