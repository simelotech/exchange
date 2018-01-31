from flask import request, jsonify, abort
from . import api
from .blockchain import get_version
#import json

@api.route('/isalive', methods=['GET'])
def isalive():
	"""
	"""
	
	version = get_version()["version"]
	
	result = {"name": "Skycoin",
			"version": version,
			"env": "ENV_INFO", #TODO: Get actual ENV_INFO content
			"isDebug": False #TODO: Should have a setting or a flag for that 
	}
	
	return jsonify(result)

