from flask import request, jsonify, abort, make_response
from . import api
from .common import build_error
import json
from .mongo import add_address_observation, delete_address_observation, get_address_list
import logging
from .. import app
from .blockchain import get_balance


@api.route('/balances/<string:address>/observation', methods=['POST'])
def add_observation(address):
    """
    Add the specified address to observation list
    """
    
    result = add_address_observation(address)
    
    #if successfully stored in observation list, return a plain 200 otherwise build error
    if "error" in result:
        return make_response(jsonify(build_error(result["error"])), result["status"])
    else:
        return ""

    
@api.route('/balances/<string:address>/observation', methods=['DELETE'])
def delete_observation(address):
    """
    Delete the specified address from observation list
    """
    
    result = delete_address_observation(address)
    
    #if successfully deleted from observation list, return a plain 200 otherwise build error
    if "error" in result:
        return make_response(jsonify(build_error(result["error"])), result["status"])
    else:
        return ""
    
    
    
    
@api.route('/balances?take=<int:take>&continuation=<string:continuation>', methods=['GET'])
@api.route('/balances?take=<int:take>', methods=['GET'])
@api.route('/balances', methods=['GET'])
def get_balances(take=0, continuation=""):
    """
    Get balances of address in observation list
    """
    
    #Get address list from mongodb
    addresses = get_address_list()
    
    items = []
    item = {}
    for addr in addresses:
        item['address'] = addr
        item['assetId'] = 0
        item['balance'] = get_balance(addr)
        item['block'] = 0 #TODO: where to get block sequence?
        items.append(item)
        
    response = {"continuation": "1234abcd", "items": items}
    
    if app.config['DEBUG']:
        logging.debug("Got balances from observation list")
        logging.debug(items)
        
    return jsonify(response)
    
    
    
     
    
    
    
    
    
    