from flask import request, jsonify, abort

from . import api
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

