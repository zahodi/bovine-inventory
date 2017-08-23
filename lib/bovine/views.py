from bovine import api
from bovine.interface import Interface
from flask import request
import json

bovine_interface = Interface()


@api.route('/api/')
def api_info():
  return json.dumps({"hello": "world"}, indent=4)


@api.route('/api/all')
def return_all():
  test_inventory = bovine_interface.get_all()
  return json.dumps(test_inventory, indent=4)


@api.route('/api/hosts', methods=['POST'])
def api_hosts():
  params = request.args
  if 'search' in params['action']:
    response_info = bovine_interface.search(inv_type='hosts', keyword=params['name'])

  return json.dumps(response_info, indent=4)


@api.route('/api/groups', methods=['POST'])
def api_groups():
  params = request.args
  if 'search' in params['action']:
    response_info = bovine_interface.search(inv_type='groups', keyword=params['name'])

  return json.dumps(response_info, indent=4)


@api.route('/api/vars', methods=['POST'])
def api_vars():
  params = request.args
  if 'list' in params['action']:
    response_info = bovine_interface.vars_list(inv_type=params['type'], keyword=params['name'])

  return json.dumps(response_info, indent=4)
