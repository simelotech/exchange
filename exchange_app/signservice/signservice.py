from flask import jsonify, request
from ..common import api, error_codes, get_transaction_from_context
from .sign_transaction import sign_transaction

@api.route('/sign', methods=['POST'])
def post_sign():
    """
    Sign transaction with private key
    """
    if not request.json:
        return make_response(jsonify(build_error('Invalid Input Format', error_codes.badFormat)), 400)

    if "privateKeys" not in request.json:
        return make_response(jsonify(build_error('Invalid Input Parameters', error_codes.missingParameter)), 400)

    if "transactionContext" not in request.json:
        return make_response(jsonify(build_error('Invalid Input Parameters', error_codes.missingParameter)), 400)

	#Private keys are ignore because they are inside wallet (which should be encrypted
    private_keys = request.json['privateKeys']
    transactionContext = request.json['transactionContext']
    transaction = get_transaction_from_context(transactionContext)
    if not transaction:
    	return make_response(jsonify(build_error('Invalid transaction context', error_codes.missingParameter)), 400)
    result = sign_transaction(transaction)
    if 'error' in result:
        return make_response(jsonify(build_error(result['error'], error_codes.unknown)), result['status'])
    return jsonify(result)
