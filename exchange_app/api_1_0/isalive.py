from flask import request, jsonify, abort
from . import api
from .blockchain import get_version
from .. import app

@api.route('/isalive', methods=['GET'])
def isalive():
	"""
	"""
	
	version = get_version()["version"]
	
	result = {"name": "Skycoin",
			"version": version,
			"env": app.config["ENVIRONMENT"], #TODO: Get actual ENV_INFO content
			"isDebug": app.config["DEBUG"]
	}
	
	return jsonify(result)

