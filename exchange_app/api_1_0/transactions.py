import logging
from flask import jsonify

from . import api
from .blockchain import get_unconfirmed_txs, get_tx_info
from .. import app


@api.route('/transactions/unconfirmed', methods=['GET'])
def transactions_unconfirmed():
    result = get_unconfirmed_txs()
    if app.config['DEBUG']:
        logging.debug("Unconfirmed Transactions")
        logging.debug(len(result))
    return jsonify(result)


@api.route('/transactions/info/<string:txid>', methods=['GET'])
def transactions_info(txid):
    result = get_tx_info(txid)
    if app.config['DEBUG']:
        logging.debug("Transaction Info")
        logging.debug(result)
    return jsonify(result)
