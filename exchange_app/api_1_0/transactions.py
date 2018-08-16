import logging
from flask import request, jsonify, make_response

from . import api
from .blockchain import create_transaction
from ..common import build_error
from ..models import add_transaction, get_transaction
from .. import app
from ..validate import validate_transaction_single, validate_transaction_many_outputs

@api.route('/transactions/single', methods=['POST'])
def transactions_single():
    tx, errormsg = validate_transaction_single(request.json)
    if not tx:
        return make_response(jsonify(build_error(errormsg)), 400)
    logging.debug('/api/transactions/single - Transaction: ' + str(tx))
    savedtx = get_transaction(tx['operationId'])
    transaction_context = False
    if savedtx:
        if 'broadcasted' in savedtx and savedtx['broadcasted']:
            logging.debug('/api/transactions/single - Transaction already broadcasted')
            return make_response("Conflict. Transaction already broadcasted", 409)
        else:
            if 'encoded_transaction' in savedtx:
                transaction_context = savedtx['encoded_transaction']
    if not transaction_context:
        result = create_transaction(tx)
        if 'error' in result:
            status = result.get('status', 500)
            return make_response(result['error'], status)
        transaction_context = result['encoded_transaction']
        add_transaction(tx['operationId'], transaction_context)
    return jsonify({"transactionContext" : transaction_context})

@api.route('/transactions/many-outputs', methods=['POST'])
def transactions_many_outputs():
    tx, errormsg = validate_transaction_many_outputs(request.json)
    if not tx:
        return make_response(jsonify(build_error(errormsg)), 400)
    logging.debug('/api/transactions/many-outputs - Transaction: ' + str(tx))
    savedtx = get_transaction(tx['operationId'])
    transaction_context = False
    if savedtx:
        if 'broadcasted' in savedtx and savedtx['broadcasted']:
            logging.debug('/api/transactions/many-outputs - Transaction already broadcasted')
            return make_response("Conflict. Transaction already broadcasted", 409)
        else:
            if 'encoded_transaction' in savedtx:
                transaction_context = savedtx['encoded_transaction']
    if not transaction_context:
        result = create_transaction(tx)
        if 'error' in result:
            return make_response(result['error'], 500)
        transaction_context = result['encoded_transaction']
    return jsonify({"transactionContext" : transaction_context})

