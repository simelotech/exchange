from flask import jsonify
from . import api
from . import blockchain


@api.route('/assets', methods=['GET'])
def get_assets():
    """
    """
    # getting data from blockchain
	
	# TODO: Must findout actual api call to get assets
	path = "/assets"
	#values = ""
	
	response_data = get_url(path)
	
	#TODO: Get data items from response and generate output
	
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


@api.route('/assets/<int:assetid>', methods=['GET'])
def get_asset(assetid):
    """
    """
    # TODO: fill with values returned from blockchain api
    retvalue = {
        "assetId": assetid,
        "address": "some address",
        "name": "asset name",
        "accuracy": "asset accuracy"
    }
    return jsonify(retvalue)
