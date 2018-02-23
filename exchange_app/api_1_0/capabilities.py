from flask import request, jsonify, abort
from . import api
#from .blockchain import spend, create_wallet
#import json

@api.route('/capabilities', methods=['GET'])
def capabilities():
	"""
	"""
	#TODO: should check with blockchain what is actually supported
	capabilities = {"isTransactionsRebuildingSupported": True,
					"areManyInputsSupported": True, 
					"areManyOutputsSupported":True
	}
	
	return jsonify(capabilities)

