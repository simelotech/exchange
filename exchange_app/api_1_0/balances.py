from flask import request, jsonify, abort, make_response
from . import api
from .common import build_error
import json
from .mongo import add_address_observation

@api.route('/balances/<string:address>/observation', methods=['POST'])
def add_observation():
    """
    Add the specified address to observation list
    """
    
    result = add_address_observation(address)
    
    #if successfully stored in observation list, return a plain 200
    if result:
        return ""
    
    return make_response(jsonify(build_error(result["error"])), result["status"])

    
@api.route('/balances/<string:address>/observation', methods=['DELETE'])
def delete_observation():
    """
    Delete the specified address from observation list
    """
    
    result = delete_address_observation(address)
    
    #if successfully stored in observation list, return a plain 200
    if result:
        return ""
    
    return make_response(jsonify(build_error(result["error"])), result["status"])