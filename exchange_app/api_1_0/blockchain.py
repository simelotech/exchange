import requests
import logging
from .. import app
from ..models import store_wallet

# TODO: Dont't hardcode this. Read from settings maybe?
base_url = "http://localhost:6420/"


def form_url(base, path):
    """
    Conform the full URL from base URL and path
    """

    if path[0] != '/':
        path = '/' + path

    if base[len(base) - 1] == '/':
        base = base[0:len(base) - 1]

    url = base + path

    return url


def get_url(path, values=""):
    """
    General GET function for blockchain
    """

    url = form_url(base_url, path)

    # resp = requests.get(url, params = values)
    # response_data = resp.json()

    response_data = {"Called": "get_url()", "url": url, "values:": values}

    return response_data


def post_url(path, values=""):
    """
    General POST function for blockchain
    """

    url = form_url(base_url, path)

    # resp = requests.post(url, data = values)
    # response_data = resp.json()

    response_data = {"Called": "post_url()", "url": url, "values:": values}

    return response_data


def create_wallet():
    """
    Create the wallet in blockchain
    """

    # generate new seed
    new_seed = requests.get(form_url(base_url, "/wallet/newSeed")).json()

    if not new_seed or "seed" not in new_seed:
        return {"status": 500, "error": "Unknown server error"}

    # generate CSRF token
    CSRF_token = requests.get(form_url(base_url, "/csrf")).json()

    if not CSRF_token or "csrf_token" not in CSRF_token:
        return {"status": 500, "error": "Unknown server error"}

    # create the wallet from seed
    # TODO: Where to get labels? How about scan?
    resp = requests.post(form_url(base_url, "/wallet/create"),
                         {"seed": new_seed["seed"],
                             "label": "wallet123", "scan": "5"},
                         headers={'X-CSRF-Token': CSRF_token['csrf_token']})

    if not resp:
        return {"status": 500, "error": "Unknown server error"}

    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}

    new_wallet = resp.json()

    if not new_wallet or "entries" not in new_wallet:
        return {"status": 500, "error": "Unknown server error"}

    # save wallet to MongoDB
    store_wallet(new_wallet)

    return {
        "privateKey": new_wallet["entries"][0]["secret_key"],
        "address": new_wallet["entries"][0]["address"]
    }


def spend(values):
    """
    Transfer balance
    """
    resp = requests.post(form_url(base_url, "/wallet/spend"), data=values)

    if not resp.json:
        return {"status": 500, "error": "Unknown server error"}

    return {"status": resp.status_code, "error": resp.json()["error"]}


def get_version():
    """
    Get blockchain version
    """

    version = requests.get(form_url(base_url, "/version"))

    if not version.json:
        return {"status": 500, "error": "Unknown server error"}

    return version.json()["version"]


def get_balance(address):
    """
    get the balance of given address in blockchain
    """

    values = {"addrs": address}
    balances = requests.get(form_url(base_url, "/balance"), params=values)

    if not balances.json:
        return {"status": 500, "error": "Unknown server error"}

    if app.config['DEBUG']:
        logging.debug("Got balance for address")
        logging.debug(balances.json())

    return balances.json()['confirmed']['coins']


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


def rebuild_transaction(values):
    """
    rebuild not signed transaction with the specified fee factor
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.put(
        form_url(base_url, "/transactions"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()


def transaction_broadcast_signed_tx(values):
    """
    broadcast the signed transaction
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.post(
        form_url(base_url, "/transactions/broadcast"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()


def transaction_broadcasted_tx(values):
    """
    return broadcasted transaction by the operationId
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.post(
        form_url(base_url, "/transactions/broadcast/single"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()


def transaction_broadcast_many_inputs(values):
    """
    return broadcasted transaction by the opreationId with many inputs
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.post(
        form_url(base_url, "/transactions/broadcast/many-inputs/"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()


def transaction_broadcast_many_outputs(values):
    """
    return broadcasted transaction by the operationId with many outputs
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.post(
        form_url(base_url, "/transactions/broadcast/many-outputs/"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()


def transaction_delete_broadcast_op(values):
    """
    remove specified transaction from the broadcasted transactions
    """
    csrf = requests.get(form_url(base_url, "/csrf")).json()
    if not csrf or "csrf_token" not in csrf:
        return {"status": 500, "error": "Unknown server error"}
    resp = requests.delete(
        form_url(base_url, "/transactions/broadcast"),
        data=values,
        headers={'X-CSRF-Token': csrf['csrf_token']}
    )
    if not resp:
        return {"status": 500, "error": "Unknown server error"}
    if resp.status_code != 200:
        return {"status": 500, "error": "Unknown server error"}
    return resp.json()
