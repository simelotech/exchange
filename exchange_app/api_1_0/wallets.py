from flask import request, jsonify, abort
from . import api
from .blockchain import get_url, post_url
import json

@api.route('/wallets', methods=['POST'])
def wallets():
	"""
	"""
	# generate new seed first
	new_seed = get_url("/wallet/newSeed") 
	new_seed = {"seed": "helmet van actor peanut"} #TODO: revove this mock response
	
	# create the wallet from seed
	values = {"seed": new_seed["seed"], "label": "wallet123", "scan": "5"} #TODO: Where to get labels? How about scan?
	new_wallet = post_url("/wallet/create", values)
	new_wallet = {"meta":{"coin": "sky", "filename": "2018-01-24-d554.wlt"}, #TODO: should we store filenames?
				  "entries":[{
					"address": "addressjdjebcjdhbjehc", 
					"public_key": "publicdwewewvefvfv",
					"secret_key": "privatewthbregvefvwef"}
					]} #TODO: remove this mock response.
	
	
	return jsonify({"address": new_wallet["entries"][0]["address"]})


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
