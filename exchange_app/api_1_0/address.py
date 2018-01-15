from flask import jsonify
from . import api


@api.route('/api/addresses/<string:address>/isvalid', methods=['GET'])
def address_valid(address):
    # TODO: validate address using blockchain api and return result
    result = True
    return jsonify({"isValid": result})
