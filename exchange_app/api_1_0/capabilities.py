from flask import jsonify
from . import api


@api.route('/capabilities', methods=['GET'])
def capabilities():
    """
    Return API capabilities set
    """

    # TODO: should check with blockchain what is actually supported
    capabilities = {
        "isTransactionsRebuildingSupported": True,
        "areManyInputsSupported": True,
        "areManyOutputsSupported": True
    }

    return jsonify(capabilities)
