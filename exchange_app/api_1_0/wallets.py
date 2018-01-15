from flask import request, jsonify, abort
from . import api


@api.route('/wallets', methods=['POST'])
def wallets():
    """
    """
    # TODO: Create wallet using blockchain api and return its address
    address = "new_wallet_address"
    return jsonify({"address": address})


@api.route('/wallets/<string:address>/cashout', methods=['POST'])
def wallets_cashout(address):
    """
    Record transaction in blockchain from wallet address to destination address in json request
    Validate request json
    """
    if not request.json \
            or "operationId" not in request.json \
            or "to" not in request.json \
            or "assetId" not in request.json \
            or "amount" not in request.json:
        abort(400)  # Bad request
    # TODO: send transfer to blockchain and get result.
    result = True

    if not result:
        abort(500)  # internal server error
    return ""
