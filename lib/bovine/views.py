from bovine import api
from bovine.interface import Interface
from flask import request
import json

bovine_interface = Interface()


@api.route('/api/')
def return_all():
  test_inventory = bovine_interface.get_all()
  return json.dumps(test_inventory, indent=4)


@api.route('/api/search', methods=['GET'])
def api_search():
  params = request.args
  if 'type' in params:
    response_info = bovine_interface.search(inv_type=params['type'], keyword=params['name'])
    return json.dumps(response_info, indent=4)


@api.route('/api/hostvars', methods=['GET'])
def api_hostvars():
  test_inventory = bovine_interface.search_host("host1")
  return json.dumps(test_inventory, indent=4)
