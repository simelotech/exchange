from .. import app
from ..settings import app_config
from ..common import build_error, form_url, get_url, post_url
import json
from ..validate import validate_sign_transaction_single
from flask import jsonify, request, make_response
import logging

def sign_transaction(tx):
    ok, errormsg = validate_sign_transaction_single(tx)
    if not ok:
        return {"status": 400, "error": errormsg}
    # generate CSRF token
    CSRF_token = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/csrf")).json()
    if not CSRF_token or "csrf_token" not in CSRF_token:
        logging.debug('sign_transaction - Error trying to get CSRF token')
        return {"status": 500, "error": "Unknown server error"}
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
    	"to": [{
        	"address": tx['toAddress'],
        	"coins": tx['amount']
         }]
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
