from flask import request, jsonify, make_response
from . import api
from .blockchain import spend, create_wallet
from ..common import build_error


@api.route('/wallets', methods=['POST'])
def wallets():
    """
    """

    result = create_wallet()

    if "publicAddress" in result:
        return jsonify(result)

    return make_response(
        jsonify(build_error(result["error"])),
        result["status"]
    )

