
import binascii
import logging
from .. import app
from ..settings import app_config
from time import perf_counter
from ..common import form_url, get_url, post_url
import skycoin
from flask import jsonify
import json

def get_version():
    """
    Get blockchain version
    """

    version = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/version"))

    if not version.json:
        return {"status": 500, "error": "Unknown server error"}

    return version.json()["version"]


def get_balance(address):
    """
    get the balance of given address in blockchain
    """

    values = {"addrs": address}
    balances = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/balance"), params=values)

    if not balances.json:
        return {"status": 500, "error": "Unknown server error"}

    if app.config['DEBUG']:
        logging.debug("Got balance for address")
        logging.debug(balances.json())

    try:
        return {'balance' : int(balances.json()['confirmed']['coins'])}
    except:
        return {"status": 500, "error": "Unknown server error"}


def get_balance_scan(address, start_block = 1):
    """
    get the balance of given address in blockchain (use block scanning)
    """

    block_count = get_block_count()

    if start_block > block_count:
        return {"status": 400, "error": "Start block higher that block height", 'block': block_count}


    blocks = get_block_range(start_block, block_count)

    if 'error' in blocks:
        return blocks

    balance = 0
    unspent_outputs = dict()

    for block in blocks:   #Scan the block range
        for txn in block['body']['txns']:

            inputs = txn['inputs']
            outputs = txn['outputs']

            #Outgoing
            balance_out = 0
            for input in inputs:
                if input in unspent_outputs:
                    balance_out += unspent_outputs.pop(input)

            #Incoming
            balance_in = 0
            for output in outputs:
                if output['dst'] == address:
                    balance_in += float(output['coins'])
                    unspent_outputs[output['uxid']] = float(output['coins'])


            balance += balance_in
            balance -= balance_out

    return {'balance': balance, 'block': block_count}


def get_block_count():
    """
    Get the current block height of blockchain
    """

    progress = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/blockchain/progress"))

    return progress.json()['current']


def get_block_range(start_block, end_block):
    """
    returns the blocks from blockchain in the specified range
    """

    values = {"start": start_block, "end": end_block}

    result = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/blocks"), params=values)

    if not result.json:
        return {"status": 500, "error": "Unknown server error"}

    return result.json()['blocks']


def get_block_by_hash(hash):
    """
    returns the blocks from blockchain in the specified range
    """

    values = {"hash": hash}

    result = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/block"), params=values)

    if not result.json:
        return {"status": 500, "error": "Unknown server error"}

    return result.json()


def get_block_by_seq(seqnum):
    """
    returns the blocks from blockchain in the specified range
    """

    values = {"seq": seqnum}

    result = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/block"), params=values)

    if not result.json:
        return {"status": 500, "error": "Unknown server error"}

    return result.json()


def get_address_transactions(address):
    """
    Return the transactions to the specified address
    """

    values = {'confirmed': 1, 'addrs': address}

    result = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/transactions"), params=values)

    if not result.json:
        return {"status": 500, "error": "Unknown server error"}

    return result.json()

def transaction_many_inputs(values):
    """
    build a transaction with many inputs
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.post(
        form_url(base_url, "/transactions/many-inputs"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()


def transaction_many_outputs(values):
    """
    build a transaction with many outputs
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.post(
        form_url(base_url, "/transactions/many-outputs"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()

def transaction_broadcast(signedTransaction):
    # generate CSRF token
    CSRF_token = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/csrf")).json()
    if not CSRF_token or "csrf_token" not in CSRF_token:
        logging.debug('transaction_broadcast - Error trying to get CSRF token')
        return {"status": 500, "error": "Unknown server error"}
    #broadcast transaction
    resp = app.lykke_session.post(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/injectTransaction"),
         json.dumps({"rawtx": signedTransaction}),
         headers={'X-CSRF-Token': CSRF_token['csrf_token']})
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    result = response.get_data(as_text=True)
    return {"result" : result}
