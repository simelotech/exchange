import json
import unittest
from exchange_app import app
import skycoin

class APITestCase(unittest.TestCase):

    exchange_prefix = "/v1/api"

    def setUp(self):
        self.app = app.test_client()

    def test_is_alive(self):
        response = self.app.get(
            self.exchange_prefix + '/isalive', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('name', json_response)
        self.assertIn('version', json_response)
        self.assertIn('env', json_response)
        self.assertIn('isDebug', json_response)
        
    def test_wallets(self):
        response = self.app.post(
            self.exchange_prefix + '/wallets',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('privateKey', json_response)
        self.assertIn('address', json_response)
        addressb58 = json_response.get("address")    
        pubkeyHex = json_response.get("privateKey") 
        address = skycoin.cipher__Address()
        error = skycoin.SKY_cipher_DecodeBase58Address(
            addressb58.encode(), address)
        self.assertEqual(error, 0)
        pubkey = skycoin.cipher_PubKey()
        error = skycoin.SKY_cipher_PubKeyFromHex(pubkeyHex.encode(), pubkey)
        self.assertEqual(error, 0)
        address2 = skycoin.cipher__Address()
        error = skycoin.SKY_cipher_AddressFromPubKey(pubkey, address2)
        self.assertEqual(error, 0)
        self.assertEqual( address.isEqual(address2), True )

if __name__ == '__main__':
    unittest.main()
