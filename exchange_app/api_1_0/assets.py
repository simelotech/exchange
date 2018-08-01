from flask import request, jsonify, make_response
from . import api
from .blockchain import get_url


@api.route('/assets', methods=['GET'])
def get_assets():
    """
    Returns skycoin assets. Just sky for now.
    """
    take = 0
    stake = request.args.get('take')
    if stake is None:
        take = 0
    else:
        try:
            take = int(stake)
        except:
            return make_response(jsonify(build_error("Invalid format : take"),
                500))
    cont = request.args.get('continuation')
    if take <= 0 or cont is not None or cont != "" :
        return jsonify({
            "continuation" : "",
            "assets": []
        })

    response_data = {
        "continuation" : "",
        "assets": [
            {
                "assetId": "sky",
                "address": "",
                "name": "Sky",
                "accuracy": "6"
            }
        ]
    }
    return jsonify(response_data)


@api.route('/assets/<string:assetid>', methods=['GET'])
def get_asset(assetid):
    """"""
    if assetid == "sky":
        retvalue = {
            "assetId": assetid,
            "address": "",
            "name": "Sky",
            "accuracy": "6"
        }

        return jsonify(response_data)
    else:
        return make_response(
            jsonify(build_error("specified asset not found"),
            204
        ))
