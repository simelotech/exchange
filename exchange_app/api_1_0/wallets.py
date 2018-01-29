from flask import request, jsonify, abort
from . import api
from .blockchain import spend, create_wallet
import json

@api.route('/wallets', methods=['POST'])
def wallets():
	"""
	"""
	
	result = create_wallet()
	
	return jsonify(result)


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
	
	values = {}
	values["id"] = address
	values["dst"] = request.json["to"]
	values["coins"] = request.json["amount"]
	
	result = spend(values)

	if result != 200:
		abort(result)  # internal server error
	
	return ""
