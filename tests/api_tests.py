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
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('continuation', json_response)
        self.assertIn('items', json_response)

        asset_record = json_response['items'][0]
        self.assertEqual(asset_record['assetId'],  'SKY')
        self.assertEqual(asset_record['address'],  '')
        self.assertEqual(asset_record['name'],     'Skycoin')
        self.assertEqual(asset_record['accuracy'], '6')

    def test_get_asset(self):
        response = self.app.get(
            '/v1/api/assets/SKY',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))

        asset_record = json_response
        self.assertEqual(asset_record['assetId'],  'SKY')
        self.assertEqual(asset_record['address'],  '')
        self.assertEqual(asset_record['name'],     'Skycoin')
        self.assertEqual(asset_record['accuracy'], '6')

    def test_get_asset_wrong_id(self):
        response = self.app.get(
            '/v1/api/assets/001',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)

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
    '''
    def test_wallets(self):
        response = self.app.post(
            '/v1/api/wallets',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('privateKey', json_response)
        self.assertIn('publicAddress', json_response)
     '''
#    def test_wallets_cashout(self):
#        # FIXME Gives 400?
#        data = dict(address=r'2GgFvqoyk9RjwVzj8tqfcXVXB4orBwoc9qv')
#        response = self.app.post(
#            '/v1/api/wallets/{}/cashout'.format(data),
#            data=json.dumps(data),
#            content_type='application/json'
#        )
#        self.assertEqual(response.status_code, 200)

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
