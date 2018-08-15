import unittest
import os
from exchange_app import app
from exchange_app.settings import app_config
import json

LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL = "http://localhost:6421/"

class LiveTestCase(unittest.TestCase):

    def setUp(self):
        self.defaultSkycoinNodeUrl = app_config.SKYCOIN_NODE_URL
        app_config.SKYCOIN_NODE_URL = LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL
        self.app = app.test_client()

    def tearDown(self):
        app_config.SKYCOIN_NODE_URL = self.defaultSkycoinNodeUrl

    def test_test(self):
        seeds_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                *('data/skycoin/seeds.json'.split('/')))
        file = open(seeds_path, "r")
        text = file.read()
        seeds = json.loads(text)
        file.close()

    def test_wallets(self):
        response = self.app.post(
            '/v1/api/wallets',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('privateKey', json_response)
        self.assertIn('publicAddress', json_response)
        self.assertIn('addressContext', json_response)
        fakeTx = {
            'operationID' : '4324432444332', #fake
            'fromAddress' : json_response['publicAddress'],
            'fromAddressContext' : json_response['addressContext'],
            'toAddress' : 'anyaddressthisshouldfail',
            'assetId' : 'SKY',
            'amount' : '1',
            'includeFee' : False
        }
        #Now tests creating a transaction
        #Result should be not enough balance
        response = self.app.post(
            '/v1/api/transactions/single',
            data = json.dumps(fakeTx),
            content_type='application/json'
        )
        self.assertNotEqual(response.status_code, 200)
        fakeTx['outputs'] = [{
            'amount' : fakeTx['amount'],
            'toAddress' : fakeTx['toAddress']
        }]
        #Now tests creating a transaction with many outputs
        #Result should be not enough balance
        response = self.app.post(
            '/v1/api/transactions/many-outputs',
            data = json.dumps(fakeTx),
            content_type='application/json'
        )
        self.assertNotEqual(response.status_code, 200)
        #Test fake sign
        data = {
            "privateKeys" : ["3434"],
            "transactionContext" : json.dumps(fakeTx)
        }
        response = self.app.post(
            '/v1/api/sign',
            data = json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 500)
        #Test fake sign
        #Test broadcasting fake transactions
        #Result should be operationID not found
        data = {
            "operationId" : '4324432444332',
            "signedTransaction" : 'faketrans',
        }
        response = self.app.post(
            '/v1/api/transactions/broadcast',
            data = json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
