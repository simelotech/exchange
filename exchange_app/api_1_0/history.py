from flask import request, jsonify, make_response
from . import api
from .common import build_error, generate_hash_key
import logging
from .. import app


@api.route('/transactions/history/from/<string:address>', methods=['GET'])
def get_history_from_address(address):
    """
    Returns completed transactions that transfer fund from the address 
    """
    
    return make_response(jsonify(build_error("Not implemented get_history_from_address")), 200)
    
    
@api.route('/transactions/history/to/<string:address>', methods=['GET'])
def get_history_to_address(address):
    """
    Returns completed transactions that transfer fund to the address 
    """
    
    return make_response(jsonify(build_error("Not implemented get_history_to_address")), 200)
    
    
@api.route('/transactions/history/from/<string:address>/observation', methods=['DELETE'])
def del_history_from_address(address):
    """
    Stops observation of the transactions that transfer fund from the address
    """
    
    result = delete_transaction_observation_from_address(address)

    # if successfully deleted from observation list, return a plain 200
    if "error" in result:
        return make_response(jsonify(build_error(result["error"])), result["status"])
    else:
        return ""
        
    
@api.route('/transactions/history/to/<string:address>/observation', methods=['DELETE'])
def del_history_to_address(address):
    """
    Stops observation of the transactions that transfer fund to the address 
    """
    
    result = delete_transaction_observation_to_address(address)

    # if successfully deleted from observation list, return a plain 200
    if "error" in result:
        return make_response(jsonify(build_error(result["error"])), result["status"])
    else:
        return ""
        

@api.route('/transactions/history/from/<string:address>/observation', methods=['POST'])
def add_history_from_address(address):
    """
    Starts observation of the transactions that transfer fund from the address 
    """
    
    result = add_transaction_observation_from_address(address)
    
    # if successfully stored in observation list, return a plain 200
    if "error" in result:
        return make_response(jsonify(build_error(result["error"])), result["status"])
    else:
        return ""
    
    
@api.route('/transactions/history/to/<string:address>/observation', methods=['POST'])
def add_history_to_address(address):
    """
    Starts observation of the transactions that transfer fund from the address
    """
    
    result = add_transaction_observation_to_address(address)
    
    # if successfully stored in observation list, return a plain 200
    if "error" in result:
        return make_response(jsonify(build_error(result["error"])), result["status"])
    else:
        return ""
    

