import re
from hashlib import sha256
from flask import jsonify
from . import api


def __decode_base58(bc, length):
    digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')


@api.route('/addresses/<string:address>/isvalid', methods=['GET'])
def address_valid(address):
    """
    Check if an address is valid
    A BTC address uses an alphanumeric base58 encoding, without 0, O, I or l.
    Important note: the last four bytes are a checksum check. They are the
    first four bytes of a double SHA-256 digest of the previous 21 bytes
    Read the first twenty-one bytes, compute the checksum, and 
    check that it corresponds to the last four bytes.
    """
    if not address.startswith(u'1') and not address.startswith(u'3'):
        result = False
    if re.match(r"[a-zA-Z1-9]{27,35}$", address) is None:
        result = False
    try:
        bcbytes = __decode_base58(address, 25)
        result = bcbytes[-4:] == sha256(sha256(bcbytes[:-4]
                                               ).digest()).digest()[:4]
    except Exception:
        result = False
    return jsonify({"isValid": result})
