from flask import jsonify, request
from . import api
from .libskycoin_interface import SignHash
from .common import error_codes

@api.route('/sign', methods=['POST'])
def post_sign():
    """
    Sign transacction with private key
    """
    if not request.json:
        return make_response(jsonify(build_error('Invalid Input Format', error_codes.badFormat)), 400)
        
    if "privateKeys" not in request.json:
        return make_response(jsonify(build_error('Invalid Input Parameters', error_codes.missingParameter)), 400)
        
    if "transactionContext" not in request.json:
        return make_response(jsonify(build_error('Invalid Input Parameters', error_codes.missingParameter)), 400)
        
    secKey = request.json['privateKeys'][0] #TODO: handle multiple keys in many inputs transactions scenario
    hash = request.json['transactionContext']
    
    signedHash = SignHash(hash, secKey)
    
    retvalue = {
        "signedTransaction": signedHash
    }
    return jsonify(retvalue)
