from flask import jsonify, make_response
import skycoin

from . import api
from ..common import build_error


def isValidAddress(address):
    """
    Validate Skycoin address.
    """
    addressObj = skycoin.cipher__Address()
    error = skycoin.SKY_cipher_DecodeBase58Address(
            address.encode(), addressObj)
    return error == 0


@api.route('/addresses/<string:address>/validity', methods=['GET'])
def address_valid(address):
    """
    Check if an address is valid
    A SKY address uses an alphanumeric base58 encoding, without 0, O, I or l.
    Important note: the last four bytes are a checksum check. They are the
    first four bytes of a double SHA-256 digest of the previous 21 bytes
    Read the first twenty-one bytes, compute the checksum, and
    check that it corresponds to the last four bytes.
    """
    return jsonify({"isValid": isValidAddress(address)})


@api.route('/addresses/<string:address>/explorer-url', methods=['GET'])
def get_explorer_url(address):
    """
    Returns explorer url for given address
    """
    if address in (None, ''):
        return make_response(jsonify(build_error('Address not specified')), 400)
    elif not isValidAddress(address):
        return make_response(jsonify(build_error('Invalid address')), 204)

    explorer_urls = ['https://explorer.skycoin.net/app/address/' + address]
    return jsonify(explorer_urls)
