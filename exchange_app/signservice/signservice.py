from flask import jsonify, request
from ..common import api
from ..common import error_codes

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

    private_keys = request.json['privateKeys']
    signedHashHex = request.json['transactionContext']
    for secKey in private_keys:
        signedHashHex = sign_hash(signedHashHex, secKey)
    return signedHashHex
