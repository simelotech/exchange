from flask import jsonify
from . import api


@api.route('/addresses/<string:address>/explorer-url', methods=['GET'])
def get_explorer_url(address):
    """
    Returns explorer url for given address
    """
    
    explorer_urls = []
    
    if address is not None:  
        url = 'https://explorer.skycoin.net/app/address/' + address
        explorer_urls.append(url)
    else:
        return make_response(jsonify(build_error('Address not specified')), 400)

    return jsonify(explorer_urls)
