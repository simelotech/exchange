import logging
from flask import request, jsonify, make_response

from . import api
from .blockchain import get_balance, get_transaction_context
from ..common import build_error
from ..models import add_transaction
from .. import app

@api.route('/api/transactions/single', methods=['POST'])
def transactions_single():
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationID', 'fromAddress', 'fromAddressContext',
            'toAddress', 'assetId', 'amount', 'includeFee'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    try:
        amount = int(request.json['amount'])
    except:
        return make_response(jsonify(build_error("Amount is not an integer")), 400)
    if request.json['assetId'] != 'sky':
        return make_response(jsonify(build_error("Only coin asset is sky")), 400)
    result = get_balance(request.json['fromAddress'])
    if 'error' in result:
        return make_response("Unknown server error", 500)
    balance = result['balance']
    if balance < amount:
        return make_response("Not enough balance", 400)
    tx = request.json
    tx = add_transaction(tx)
    if not tx:
        return make_response("Unknown server error", 500)
    elif tx['broadcasted']:
    	return make_response("Conflict. Transaction already broadcasted", 409)
    transaction_context = get_transaction_context(tx)
    return jsonify({"transactionContext" : transaction_context})

'''
@api.route('/api/transactions/many-inputs', methods=['POST'])
def transactions_many_inputs():
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationID', 'inputs', 'toAddress', 'assetId'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = transaction_many_inputs(request.json)
    if "transactionContext" in result:
        return jsonify(result)
    return jsonify({"status": 500, "error": "Invalid response"})


@api.route('/api/transactions/many-outputs', methods=['POST'])
def transactions_many_outputs():
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationId', 'fromAddress', 'fromAddressContext', 'outputs', 'assetId'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    tx = add_many_outputs_tx(request.json)
    if tx:
        result = transaction_many_outputs(request.json)
        if "transactionContext" in result:
            return jsonify(result)
        if app.config['DEBUG']:
            logging.debug("Transaction: %s", request.args.get('operationId'))
    return jsonify({"status": 500, "error": "Invalid response"})
'''
