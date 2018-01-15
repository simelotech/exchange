from flask import request, jsonify, abort
from . import api


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
