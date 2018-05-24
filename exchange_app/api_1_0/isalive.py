from flask import jsonify, make_response
from . import api
from .blockchain import get_version
from .. import app
from .common import build_error


@api.route('/isalive', methods=['GET'])
def isalive():
    """
    Return some general service info. Used to check if service is running
    """

    version = get_version()

    if "error" in version:
        return make_response(
            jsonify(build_error(version["error"])),
            version["status"]
        )

    result = {
        "name": "Skycoin",
        "version": version,  # TODO: Return skycoin version or this API version?
        "env": app.config["ENVIRONMENT"],
        "isDebug": app.config["DEBUG"]
    }

    return jsonify(result)
