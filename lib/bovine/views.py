from bovine import api
from bovine.interface import Interface
from flask import request
import json

bovine_interface = Interface()


@api.route('/api/')
def return_all():
  test_inventory = bovine_interface.get_all()
  return json.dumps(test_inventory, indent=4)


@api.route('/api/hosts', methods=['POST'])
def api_host():
  params = request.args
  if 'search' in params['action']:
    response_info = bovine_interface.search(inv_type='hosts', keyword=params['name'])

  return json.dumps(response_info, indent=4)


@api.route('/api/groups', methods=['POST'])
def api_group():
  params = request.args
  if 'search' in params['action']:
    response_info = bovine_interface.search(inv_type='groups', keyword=params['name'])

  return json.dumps(response_info, indent=4)
