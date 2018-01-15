from flask import request, jsonify, abort
from . import api


@api.route('/api/assets', methods=['GET'])
def get_assets():
    """"""
    # TODO: fill with values returned from blockchain api
    retvalue = {
        "assets": [
            {
                "assetId": "1234",
                "address": "some address",
                "name": "asset name",
                "accuracy": "asset accuracy"
            },
            {
                "assetId": "5678",
                "address": "some address",
                "name": "asset name",
                "accuracy": "asset accuracy"
            }
        ]
    }
    return jsonify(retvalue)


@api.route('/api/assets/<int:assetid>', methods=['GET'])
def get_asset(assetid):
    """"""
    # TODO: fill with values returned from blockchain api
    retvalue = {
        "assetId": assetid,
        "address": "some address",
        "name": "asset name",
        "accuracy": "asset accuracy"
    }
    return jsonify(retvalue)


@api.route('/api/addresses/<string:address>/isvalid', methods=['GET'])
def address_valid(address):
    # TODO: validate address using blockchain api and return result
    result = True
    return jsonify({"isValid": result})


@api.route('/api/wallets', methods=['POST'])
def wallets():
    # TODO: Create wallet using blockchain api and return its address
    address = "new_wallet_address"
    return jsonify({"address": address})


@api.route('/api/wallets/<string:address>/cashout', methods=['POST'])
def wallets_cashout(address):
    """
    Record transaction in blockchain from wallet address to destination address in json request
    Validate request json
    """
    if not request.json \
            or not "operationId" in request.json \
            or not "to" in request.json \
            or not "assetId" in request.json \
            or not "amount" in request.json:
        abort(400)  # Bad request
    # TODO: send transfer to blockchain and get result.
    result = True

    if not result:
        abort(500)  # internal server error
    return ""


@api.route('/api/pending-events/cashin', methods=['GET', 'DELETE'])
def pending_events_cashin():
    """
    """
    if request.method == 'GET':  # GET handler
        max_events_number = request.args.get('maxEventsNumber', '')
        # TODO: Return up to maxEventsNumber results from blockchain
        retvalue = {
            "events": [
                {
                    "operationId": "1234",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 1000000
                },
                {
                    "operationId": "5678",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 2000000
                }
            ]
        }
        return jsonify(retvalue)
    if request.method == 'DELETE':  # DELETE handler
        # Remove pending “cashin” events with specified operation ids
        # Validate request json
        if not request.json \
                or not "operationIds" in request.json:
            abort(400)  # Bad request
            # TODO: delete specified operation ids from blockchain and get result.
        result = True
        if not result:
            abort(500)  # internal server error
        return ""


@api.route('/api/pending-events/cashout-started', methods=['GET', 'DELETE'])
def pending_events_cashout_started():
    if request.method == 'GET':  # GET handler
        max_events_number = request.args.get('maxEventsNumber', '')
        # TODO:Return up to maxEventsNumber results from blockchain
        retvalue = {
            "events": [
                {
                    "operationId": "1234",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 1000000
                },
                {
                    "operationId": "5678",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 2000000
                }
            ]
        }
        return jsonify(retvalue)
    if request.method == 'DELETE':  # DELETE handler
        # Remove pending "cashout started" events with specified operation ids
        # Validate request json
        if not request.json \
                or not "operationIds" in request.json:
            abort(400)  # Bad request
        # TODO: delete specified operation ids from blockchain and get result.
        result = True
        if not result:
            abort(500)  # internal server error
        return ""


@api.route('/api/pending-events/cashout-completed', methods=['GET', 'DELETE'])
def pending_events_cashout_completed():
    """
    """
    # GET handler
    if request.method == 'GET':
        max_events_number = request.args.get('maxEventsNumber', '')
        # TODO:Return up to maxEventsNumber results from blockchain
        retvalue = {
            "events": [
                {
                    "operationId": "1234",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 1000000
                },
                {
                    "operationId": "5678",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 2000000
                }
            ]
        }
        return jsonify(retvalue)

    if request.method == 'DELETE':  # DELETE handler
        # Remove pending "cashout completed" events with specified operation ids
        # Validate request json
        if not request.json \
                or not "operationIds" in request.json:
            abort(400)  # Bad request
        # TODO: delete specified operation ids from blockchain and get result.
        result = True
        if not result:
            abort(500)  # internal server error
        return ""


@api.route('/api/pending-events/cashout-failed', methods=['GET', 'DELETE'])
def pending_events_cashout_failed():
    # GET handler
    if request.method == 'GET':
        max_events_number = request.args.get('maxEventsNumber', '')
        # TODO:Return up to maxEventsNumber results from blockchain
        retvalue = {
            "events": [
                {
                    "operationId": "1234",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 1000000
                },
                {
                    "operationId": "5678",
                    "timestamp": "ISO 8601 event moment",
                    "assetId": "USD",
                    "amount": 2000000
                }
            ]
        }
        return jsonify(retvalue)
    if request.method == 'DELETE':  # DELETE handler
        # Remove pending "cashout failed" events with specified operation ids
        # Validate request json
        if not request.json \
                or not "operationIds" in request.json:
            abort(400)  # Bad request
        # TODO: delete specified operation ids from blockchain and get result.
        result = True
        if not result:
            abort(500)  # internal server error
        return ""
