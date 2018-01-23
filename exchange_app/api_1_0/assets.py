from flask import jsonify
from . import api
from . import blockchain


@api.route('/api/v1.0/assets', methods=['GET'])
def get_assets():
    """
    """
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


@api.route('/api/v1.0/assets/<int:assetid>', methods=['GET'])
def get_asset(assetid):
    """
    """
    
	# getting data from blockchain
	
	# TODO: Must findout actual api call to get assets
	path = "/assets"
	values[id] = assetid
	
	response_data = get_url(path, values)
	
	#TODO: Get data items from response and generate output
	
    retvalue = {
        "assetId": assetid,
        "address": "some address",
        "name": "asset name",
        "accuracy": "asset accuracy"
    }
    return jsonify(retvalue)
