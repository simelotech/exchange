from skycoin import cipher__Address, SKY_cipher_DecodeBase58Address
from flask import jsonify
from . import api


@api.route('/addresses/<string:address>/validity', methods=['GET'])
def address_valid(address):
    result = True if SKY_cipher_DecodeBase58Address(
        address.encode(), cipher__Address()) == 0 else False
    return jsonify({"isValid": result})
