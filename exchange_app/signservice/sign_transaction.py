from .. import app
from ..settings import app_config
from ..common import build_error, form_url, get_url, post_url
import json
from ..validate import validate_sign_transaction
from flask import jsonify, request, make_response
import logging
import codecs
import skycoin

def sign_transaction(txContext, privateKeys):
    transaction_handle = 0
    try:
        serialized = codecs.decode(txContext, 'hex')
        error, transaction_handle = skycoin.SKY_coin_TransactionDeserialize(serialized)
        if error != 0:
            logging.debug('sign_transaction - Error deserializing transaction context')
            return {"status": 500, "error": "Error deserializing transaction context"}
        secKeys = []
        for key in privateKeys:
            seckey = skycoin.cipher_SecKey()
            error = skycoin.SKY_cipher_SecKeyFromHex(key.encode(), seckey)
            if error != 0:
                logging.debug('sign_transaction - Error parsing hex sec key')
                return {"status": 500, "error": "Error parsing hex sec key"}
            secKeys.append(seckey)
        error = skycoin.SKY_coin_Transaction_SignInputs(transaction_handle, secKeys)
        if error != 0:
            logging.debug('sign_transaction - Error signing transaction')
            return {"status": 500, "error": "Error signing transaction"}
        error, serialized = skycoin.SKY_coin_Transaction_Serialize(transaction_handle)
        if error != 0:
            logging.debug('sign_transaction - Error serializing transaction')
            return {"status": 500, "error": "Error serializing transaction"}
        newContext = codecs.encode(serialized, 'hex')
        return {"signedTransaction" : newContext}
    except:
        return {"status": 500, "error": "Unknown Error"}
    finally:
        if transaction_handle != 0:
            skycoin.SKY_handle_close(handle)

'''
def sign_transaction(tx):
    ok, errormsg = validate_sign_transaction(tx)
    if not ok:
        return {"status": 400, "error": errormsg}
    # generate CSRF token
    CSRF_token = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/csrf")).json()
    if not CSRF_token or "csrf_token" not in CSRF_token:
        logging.debug('sign_transaction - Error trying to get CSRF token')
        return {"status": 500, "error": "Unknown server error"}
    outputs = []
    for output in tx['outputs']:
        dest = {
        	"address": output['toAddress'],
        	"coins": output['amount']
        }
        outputs.append(dest)
    data = {
    	"hours_selection": {
        	"type": "auto",
        	"mode": "share",
        	"share_factor": "0.5"
    	},
    	"wallet": {
        	"id": tx['fromAddressContext'],
        	"addresses": [tx['fromAddress']],
    	},
    	"to": outputs
    }
    response = app.lykke_session.post(form_url(app_config.SKYCOIN_NODE_URL,
            '/api/v1/wallet/transaction'),
            data=json.dumps(data),
            headers={'X-CSRF-Token': CSRF_token['csrf_token']})
    if response.status_code == 200:
        json_response = json.loads(response.get_data(as_text=True))
        if not 'error' in json_response:
            if 'encoded_transaction' in json_response:
                return {"signedTransaction" : json_response['encoded_transaction']}
        logging.debug('sign_transaction - Invalid response from create transaction"}')
        return {"status": 500, "error": "Invalid response from create transaction"}
    else:
        logging.debug('sign_transaction - Error creating transaction in Skycoin')
        return {"status": 500, "error": "Error creating transaction in Skycoin"}
'''
