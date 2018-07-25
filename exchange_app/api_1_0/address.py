from flask import jsonify
from . import api
from .libskycoin_interface import DecodeBase58Address


@api.route('/addresses/<string:address>/validity', methods=['GET'])
def address_valid(address):
    """
    Check if an address is valid
    A BTC address uses an alphanumeric base58 encoding, without 0, O, I or l.
    Important note: the last four bytes are a checksum check. They are the
    first four bytes of a double SHA-256 digest of the previous 21 bytes
    Read the first twenty-one bytes, compute the checksum, and
    check that it corresponds to the last four bytes.
    """


    try:
        if DecodeBase58Address(address)[0] == 0:
             result = True
        else:
             result = False

    except Exception:
        raise
        result = False

    return jsonify({"isValid": result})
