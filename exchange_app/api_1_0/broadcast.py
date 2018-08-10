import logging
from flask import request, jsonify, make_response
from . import api
from .. import app
from ..validate import validate_transaction_broadcast
from ..models import get_transaction
from .blockchain import transaction_broadcast
from ..common import build_error

@api.route('/transactions/broadcast', methods=['POST'])
def transactions_broadcast():
    """
    Broadcast transaction
    """
    ok, errormsg = validate_transaction_broadcast(request.json)
    if not ok:
        return make_response(jsonify(build_error(errormsg)), 400)
    tx = get_transaction(request.json["operationId"])
    if not tx:
        #TODO: We could broadcast the transaction anyway
        return make_response(jsonify(build_error("Operation Id doesn\'t match a transaction")), 400)
    if 'broadcasted' in tx and tx['broadcasted']:
        return make_response(jsonify(build_error("Transaction already broadcasted")), 409)
    signedTransaction = request.json['signedTransaction']
    result = transaction_broadcast(signedTransaction)
    if 'error' in result:
        return make_response(jsonify(build_error(result['error'])), 400)
    return jsonify(result)
