from flask import request, jsonify, make_response

from . import api
from .blockchain import transaction_many_inputs, transaction_many_outputs, rebuild_transaction, transaction_broadcast_signed_tx, transaction_broadcasted_tx, transaction_broadcast_many_inputs, transaction_broadcast_many_outputs, transaction_delete_broadcast_op
from .common import build_error


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
    params = {'operationID', 'fromAddress', 'fromAddressContext', 'outputs', 'assetId'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = transaction_many_outputs(request.json)
    if "transactionContext" in result:
        return jsonify(result)
    return jsonify({"status": 500, "error": "Invalid response"})


@api.route('/api/transactions', methods=['PUT'])
def rebuild_transactions():
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationId', 'feeFactor'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = rebuild_transaction(request.json)
    if "transactionContext" in result:
        return jsonify(result)
    return jsonify({"status": 500, "error": "Invalid response"})


@api.route('/api/transactions/broadcast', methods=['POST'])
def broadcast_signed_tx():
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationId', 'signedTransaction'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = transaction_broadcast_signed_tx(request.json)
    return jsonify(result)


@api.route(' /api/transactions/broadcast/single/<int:operationId>', methods=['GET'])
def broadcasted_tx(operationId):
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationId'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = transaction_broadcasted_tx(request.json)
    return jsonify(result)


@api.route(' /api/transactions/broadcast/many-inputs/<int:operationId>', methods=['GET'])
def broadcasted_many_inputs(operationId):
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationId'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = transaction_broadcast_many_inputs(request.json)
    return jsonify(result)


@api.route(' /api/transactions/broadcast/many-outputs/<int:operationId>', methods=['GET'])
def broadcasted_many_outputs(operationId):
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationId'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = transaction_broadcast_many_outputs(request.json)
    return jsonify(result)


@api.route(' /api/transactions/broadcast/<int:operationId>', methods=['DELETE'])
def delete_broadcasted_op(operationId):
    if not request.json:
        return make_response(jsonify(build_error("Input format error")), 400)
    params = {'operationId'}
    if all(x not in params for x in request.json):
        return make_response(jsonify(build_error("Input data error")), 400)
    result = transaction_delete_broadcast_op(request.json)
    return jsonify(result)
