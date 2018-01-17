from flask import jsonify, request
from . import api


@api.route('/wallets', methods=['POST'])
def post_wallets():
    """
    """
    
	# TODO: fill with values returned from blockchain api
    retvalue = {
        "privateKey": "superprivatekey",
		"publicAddress": "the address"
    }
    return jsonify(retvalue)


@api.route('/sign', methods=['POST'])
def post_sign():
    """
    """
    if not request.json \
            or "privateKey" not in request.json \
            or "transactionHex" not in request.json:
        abort(400)  # Bad request
		
	# TODO: fill with values returned from blockchain api
	signed_data = "(^_^)"
    retvalue = {
        "signedTransaction": signed_data
    }
    return jsonify(retvalue)
