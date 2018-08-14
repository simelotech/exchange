from flask import request, jsonify, make_response

from . import api
from ..common import build_error
from ..settings import app_config

@api.route('/capabilities', methods=['GET'])
def capabilities():
    """
    Return API capabilities set
    """
    
    capabilities = {"isTransactionsRebuildingSupported": False,
                    "areManyInputsSupported": not app_config.SKYCOIN_WALLET_SHARED,
                    "areManyOutputsSupported": True,
                    "isTestingTransfersSupported": False,
                    "isPublicAddressExtensionRequired": False,
                    "isReceiveTransactionRequired": False,
                    "canReturnExplorerUrl": True
    }
    
    return jsonify(capabilities)


@api.route('/constants', methods=['GET'])
def constants():
    """
    API constants not implemented
    """
    return make_response(jsonify(build_error('No constants in Skycoin Blockchain API')), 501)
    
