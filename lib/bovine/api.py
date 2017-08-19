from bovine import bovine
from bovine.interface import Interface
from flask import request
import json
import requests


bovine_interface = Interface()


@bovine.route('/bovine-api/')
def setUp():
  test_inventory = Interface.get_all()
  return json.dumps(test_inventory, indent=4)


@bovine.route('/bovine-api/search', methods=['GET'])
def api_search():
  test_inventory = bovine_interface.search("host1")
  return json.dumps(test_inventory, indent=4)


@bovine.route('/bovine-api/hostvars', methods=['GET'])
def api_hostvars():
  test_inventory = bovine_interface.search_host("host1")
  return json.dumps(test_inventory, indent=4)


@bovine.route('/bovine-api/hello', methods=['GET'])
def hello():
  return request.args['name']
