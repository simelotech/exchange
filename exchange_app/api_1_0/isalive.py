from flask import jsonify, make_response
from . import api
from .blockchain import get_version
from .. import app
from ..common import build_error

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
        "name": app.config['SKYCOIN_FIBER_NAME'],
        "version": version,
        "env": app.config["ENVIRONMENT"],
        "isDebug": app.config["DEBUG"],
        "contractVersion": app.config['LYKKE_API_VERSION']
    }

    return jsonify(result)
