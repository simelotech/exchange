from flask import request, jsonify, abort
from . import api

@api.route('/capabilities', methods=['GET'])
def capabilities():
    """
    Return API capabilities set
    """
    
    #TODO: should check with blockchain what is actually supported
    capabilities = {"isTransactionsRebuildingSupported": False,
                    "areManyInputsSupported": True, 
                    "areManyOutputsSupported": True,
                    "isTestingTransfersSupported": True,
                    "isPublicAddressExtensionRequired": False,
                    "isReceiveTransactionRequired": False,
                    "canReturnExplorerUrl": False
    }
    
    return jsonify(capabilities)

