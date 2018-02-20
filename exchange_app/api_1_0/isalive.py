from flask import request, jsonify, abort, make_response
from . import api
from .blockchain import get_version
from .. import app
from .common import build_error

@api.route('/isalive', methods=['GET'])
def isalive():
	"""
	"""
	
	version = get_version()
    
    if version['error']
        return make_response(jsonify(build_error(version["error"])), version["status"])
	
	result = {"name": "Skycoin",
			"version": version, #TODO: Return skycoin version or this API version?
			"env": app.config["ENVIRONMENT"],
			"isDebug": app.config["DEBUG"]
	}
	
	return jsonify(result)

