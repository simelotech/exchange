from .. import app
from ..settings import app_config
from ..common import form_url, get_url, post_url
import json
from ..validate import validate_sign_transaction_single

def sign_transaction(tx):
    ok, errormsg = validate_sign_transaction_single(request.json)
    if not ok:
        return make_response(jsonify(build_error(errormsg)), 400)
	# generate new seed
    new_seed = app.lykke_session.get(
        form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/wallet/newSeed?entropy=128")).json()
    if not new_seed or "seed" not in new_seed:
        logging.debug('sign_transaction - Error creating seed')
        return {"status": 500, "error": "Unknown server error"}
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
            headers={'X-CSRF-Token': CSRF_token['csrf_token']},
            content_type='application/json')
    if response.status_code == 200:
        json_response = json.loads(response.get_data(as_text=True))
        if not 'error' in json_response:
            if 'encoded_transaction' in json_response:
                return {"signedTransaction" : json_response['encoded_transaction']}
            else:
                logging.debug('sign_transaction - Invalid response from create transaction"}')
                return {"status": 500, "error": "Invalid response from create transaction"}
        else:
            logging.debug('sign_transaction - Error from skycoin: ' + response.message)
            return {"status": response.status_code, "error": response.message}
