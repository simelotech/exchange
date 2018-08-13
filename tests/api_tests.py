import binascii
import json
import unittest

import skycoin

from exchange_app import app
from exchange_app.settings import app_config

# Removed endpoints
URL_PENDING_EVENTS_CASHIN            = '/v1/api/pending-events/cashin'
URL_PENDING_EVENTS_CASHOUT_START     = '/v1/api/pending-events/cashout-started'
URL_PENDING_EVENTS_CASHOUT_COMPLETED = '/v1/api/pending-events/cashout-completed'
URL_PENDING_EVENTS_CASHOUT_FAILED    = '/v1/api/pending-events/cashout-failed'
URL_WALLET_CASHOUT                   = '/v1/api/wallets/{address}/cashout'
# Current API
URL_ADDRESS_VALIDITY = '/v1/api/addresses/{address}/validity'
URL_BALANCE_ADDRESS  = '/v1/api/balances/{address}/observation'
URL_ASSETS           = '/v1/api/assets'
URL_ASSET            = '/v1/api/assets/{id}'
URL_WALLET_NEW       = '/v1/api/wallets'
URL_ISALIVE          = '/v1/api/isalive'
URL_CAPABILITIES     = '/v1/api/capabilities'
URL_SIGN             = '/v1/api/sign'
URL_CONSTANTS        = '/v1/api/constants'
URL_EXPLORER         = '/v1/api/addresses/{address}/explorer-url'

ADDRESS_VALID = r'2GgFvqoyk9RjwVzj8tqfcXVXB4orBwoc9qv'
ADDRESS_INVALID = r'12345678'


class BaseApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()


class ApiTestCase(BaseApiTestCase):
    def test_address_valid(self):
        address = ADDRESS_VALID
        response = self.app.get(URL_ADDRESS_VALIDITY.format(address=address))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['isValid'], True)

    def test_address_invalid(self):
        address = ADDRESS_INVALID
        response = self.app.get(URL_ADDRESS_VALIDITY.format(address=address))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['isValid'], False)

    def test_get_assets(self):
        response = self.app.get(URL_ASSETS, content_type='application/json')
            
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
        response = self.app.get(URL_ASSET.format(id='SKY'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))

        asset_record = json_response
        self.assertEqual(asset_record['assetId'],  'SKY')
        self.assertEqual(asset_record['address'],  '')
        self.assertEqual(asset_record['name'],     'Skycoin')
        self.assertEqual(asset_record['accuracy'], '6')

    def test_get_asset_wrong_id(self):
        response = self.app.get(URL_ASSET.format(id='UNKCOIN'), content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_wallets(self):
        response = self.app.post(URL_WALLET_NEW, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('privateKey', json_response)
        self.assertIn('publicAddress', json_response)
        seckey = skycoin.cipher_SecKey()
        err = skycoin.SKY_cipher_NewSecKey(binascii.unhexlify(json_response['privateKey']), seckey)
        self.assertEqual(err, 0)
        address = skycoin.cipher__Address()
        err = skycoin.SKY_cipher_AddressFromSecKey(seckey, address)
        self.assertEqual(err, 0)
        err, addressStr = skycoin.SKY_cipher_Address_String(address)
        self.assertEqual(err, 0)
        self.assertEqual(addressStr.decode('ascii'), json_response['publicAddress'])

    def test_is_alive(self):
        response = self.app.get(URL_ISALIVE, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('name', json_response)
        self.assertIn('version', json_response)
        self.assertIn('env', json_response)
        self.assertIn('isDebug', json_response)

    def test_api_capabilities(self):
        response = self.app.get(URL_CAPABILITIES, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('isTransactionsRebuildingSupported', json_response)
        self.assertIn('areManyInputsSupported', json_response)
        self.assertIn('areManyOutputsSupported', json_response)
        self.assertIn("isTestingTransfersSupported", json_response)
        self.assertIn("isPublicAddressExtensionRequired", json_response)
        self.assertIn("isReceiveTransactionRequired", json_response)
        self.assertIn("canReturnExplorerUrl", json_response)
        self.assertEqual(json_response['isTransactionsRebuildingSupported'], False)
        self.assertEqual(json_response['areManyInputsSupported'], not app_config.SKYCOIN_WALLET_SHARED)
        self.assertEqual(json_response['areManyOutputsSupported'], True)
        self.assertEqual(json_response['isTestingTransfersSupported'], False)
        self.assertEqual(json_response['isPublicAddressExtensionRequired'], False)
        self.assertEqual(json_response['isReceiveTransactionRequired'], False)
        self.assertEqual(json_response['canReturnExplorerUrl'], True)
        
    def test_sign_noparams(self):
        response = self.app.post(URL_SIGN, content_type='application/json')
        #test response code is 400 without parameters
        self.assertEqual(response.status_code, 400)

    def test_constants(self):
        response = self.app.get(URL_CONSTANTS, content_type='application/json')
        #test constants not implemented
        self.assertEqual(response.status_code, 501)

    def test_explorer_url(self):
        response = self.app.get(URL_EXPLORER.format(address=ADDRESS_VALID), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertListEqual(json_response,
                ['https://explorer.skycoin.net/app/address/2GgFvqoyk9RjwVzj8tqfcXVXB4orBwoc9qv'])

    def test_explorer_url_noaddr(self):
        response = self.app.get(URL_EXPLORER.format(address=''), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_explorer_url_invalid(self):
        response = self.app.get(URL_EXPLORER.format(address=ADDRESS_INVALID), content_type='application/json')
        self.assertEqual(response.status_code, 204)


class DeprecatedApiTests(BaseApiTestCase):

    def assert_get_not_found(self, template, **args):
        url = template.format(**args)
        response = self.app.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_pending_events_cashin(self):
        self.assert_get_not_found(URL_PENDING_EVENTS_CASHIN)

    def test_pending_events_cashout_started(self):
        self.assert_get_not_found(URL_PENDING_EVENTS_CASHOUT_START)

    def test_pending_events_cashout_completed(self):
        self.assert_get_not_found(URL_PENDING_EVENTS_CASHOUT_COMPLETED)

    def test_pending_events_cashout_failed(self):
        self.assert_get_not_found(URL_PENDING_EVENTS_CASHOUT_FAILED)

    def test_wallets_cashout(self):
        self.assert_get_not_found(URL_WALLET_CASHOUT,address=r'2GgFvqoyk9RjwVzj8tqfcXVXB4orBwoc9qv')


if __name__ == '__main__':
    unittest.main()
