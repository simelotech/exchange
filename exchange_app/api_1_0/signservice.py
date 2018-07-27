from flask import jsonify, request
from . import api
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

    seckeyHex = request.json['privateKeys'][0] #TODO: handle multiple keys in many inputs transactions scenario
    hashHex = request.json['transactionContext']

    return sign_hash(hashHex, seckeyHex)
