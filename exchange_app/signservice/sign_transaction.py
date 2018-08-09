from .. import app
from ..settings import app_config
from ..common import form_url, get_url, post_url
import json

def sign_transaction(tx):
	# generate new seed
    new_seed = app.lykke_session.get(
        form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/wallet/newSeed?entropy=128")).json()

    if not new_seed or "seed" not in new_seed:
        logging.debug('sign_transaction - Error creating seed')
        return {"status": 500, "error": "Unknown server error"}
    params = {'operationID', 'fromAddress', 'fromAddressContext',
            'toAddress', 'assetId', 'amount', 'includeFee'}
    if all(x not in params for x in tx):
        logging.debug('sign_transaction - Invalid transaction context')
        return {"status": 400, "error": "Invalid transaction context"}
    if request.json['assetId'] != 'sky':
        logging.debug('sign_transaction - Only coin is sky')
        return {"status": 400, "error": "Only coin is sky"}
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
