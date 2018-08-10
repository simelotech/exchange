import json
import unittest
from exchange_app import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_address_valid(self):
        address= r'2GgFvqoyk9RjwVzj8tqfcXVXB4orBwoc9qv'
        response = self.app.get(
            '/v1/api/addresses/{}/validity'.format(address)
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['isValid'], True)

    def test_address_invalid(self):
        address = r'12345678'
        response = self.app.get(
            '/v1/api/addresses/{}/validity'.format(address)
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['isValid'], False)

    def test_get_assets(self):
        response = self.app.get(
            '/v1/api/assets', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_asset(self):
    	#TODO: Fix, this is wrong, asset id is passed as parameter
        data = dict(assetid=1)
        response = self.app.get(
            '/v1/api/assets',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashin(self):
        response = self.app.get(
            '/v1/api/pending-events/cashin',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashout_started(self):
        response = self.app.get(
            '/v1/api/pending-events/cashout-started',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashout_completed(self):
        response = self.app.get(
            '/v1/api/pending-events/cashout-completed',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashout_failed(self):
        response = self.app.get(
            '/v1/api/pending-events/cashout-failed',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

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
            'operationID' : '43244324', #fake
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
        self.assertEqual(response.status_code, 400)
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
            "operationId" : '43244324',
            "signedTransaction" : 'faketrans',
        }
        response = self.app.post(
            '/v1/api/transactions/broadcast',
            data = json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_is_alive(self):
        response = self.app.get(
            '/v1/api/isalive', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('name', json_response)
        self.assertIn('version', json_response)
        self.assertIn('env', json_response)
        self.assertIn('isDebug', json_response)

    def test_api_capabilities(self):
        response = self.app.get(
            '/v1/api/capabilities', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('isTransactionsRebuildingSupported', json_response)
        self.assertIn('areManyInputsSupported', json_response)
        self.assertIn('areManyOutputsSupported', json_response)

    def test_sign(self):
        pass
        response = self.app.post(
            '/v1/api/sign', content_type='application/json')
        #test response code is 400 without parameters
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
