import unittest
import os
from exchange_app import app
from exchange_app.settings import app_config
import json
import skycoin
import binascii
import urllib.request
import time
import logging
import codecs

LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL = "http://localhost:6421/"

class LiveTestCase(unittest.TestCase):

    def setUp(self):
        self.defaultSkycoinNodeUrl = app_config.SKYCOIN_NODE_URL
        app_config.SKYCOIN_NODE_URL = LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL
        self.app = app.test_client()
        #Wait for service to finish checking database (too big)
        time.sleep(10)
        self.serverUp = False
        self.wallets = self._createTestWallets()
        self.addressWithBalance = ""
        self.addressWithoutBalance = ""
        self.pickAddresses()

    def tearDown(self):
        app_config.SKYCOIN_NODE_URL = self.defaultSkycoinNodeUrl

    def pickAddresses(self):
        values = {"addrs": ",".join(self.wallets.keys())}
        balances = app.lykke_session.get(self.form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/balance"), params=values)
        if not balances.json:
            raise Exception("Error when getting wallet balances")

        response = balances.json()
        if "error" in response:
            raise Exception(response["error"]["message"])
        keys = response["addresses"].keys()
        self.addressWithBalance = ""
        self.addressWithoutBalance = ""
        for key in keys:
            coins = response["addresses"][key]["confirmed"]["coins"]
            if coins > 0:
                self.addressWithBalance = key
            else:
                self.addressWithoutBalance = key
        assert self.addressWithBalance != "", "No wallet with balance"
        assert self.addressWithoutBalance != "", "No wallet with 0 balance"

    def test_transaction_single(self):
        sourceAddress = self.addressWithBalance
        sourceWallet = self.wallets[sourceAddress]["addressContext"]
        privateKey = self.wallets[sourceAddress]["privateKey"]
        destAddress = self.addressWithoutBalance
        testTx = {
            'operationID' : '4324432444332', #just some operation id
            'fromAddress' : sourceAddress,
            'fromAddressContext' : sourceWallet,
            'toAddress' : destAddress,
            'assetId' : 'SKY',
            'amount' : '1',
            'includeFee' : False
        }
        response = self.app.post(
            '/v1/api/transactions/single',
            data = json.dumps(testTx),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('transactionContext', json_response)
        transaction_context = json_response['transactionContext']
        #Test transaction sign
        data = {
            "privateKeys" : [privateKey],
            "transactionContext" : transaction_context
        }
        response = self.app.post(
            '/v1/api/sign',
            data = json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('signedTransaction', json_response)
        #Test deserializing back the signed transaction
        serialized = codecs.decode(json_response['signedTransaction'], 'hex')
        error, transaction_handle = skycoin.SKY_coin_TransactionDeserialize(serialized)
        assert error == 0, "Error deserializing signed transaction"
        assert transaction_handle != 0, "Invalid handle returned from SKY_coin_TransactionDeserialize"
        skycoin.SKY_handle_close(transaction_handle)

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
    '''

    def _createTestWallets(self):
        seeds_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                *('data/skycoin/seeds.json'.split('/')))
        file = open(seeds_path, "r")
        text = file.read()
        r = json.loads(text)
        file.close()
        wallets = {}
        for seed in r["seeds"]:
            wallet = self._createWalletFromSeed(seed)
            wallets[wallet["publicAddress"]] = wallet
        return wallets

    def _getCSRFToken(self):
        # generate CSRF token
        tries = 1
        if not self.serverUp:
            tries = 10
        timeOut = 10
        CSRF_token = False
        while tries > 0:
            try:
                CSRF_token = app.lykke_session.get(self.form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/csrf")).json()
            except:
                logging.debug("Error requesting csrf token")
                time.sleep(timeOut)
            tries -= 1
        if not CSRF_token or "csrf_token" not in CSRF_token:
            assert False, "Error requesting token"
        self.serverUp = True
        return CSRF_token

    def _createWalletFromSeed(self, seed):
        CSRF_token = self._getCSRFToken()
        # create the wallet from seed
        resp = app.lykke_session.post(self.form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/wallet/create"),
                             {"seed": seed,
                                 "label": "wallet123", "scan": "5"},
                             headers={'X-CSRF-Token': CSRF_token['csrf_token']})

        if not resp:
            raise Exception("No response when creating wallet")

        if resp.status_code != 200:
            raise Exception("Error {0} when creating wallet".format(resp.status_code))

        new_wallet = resp.json()

        if not new_wallet or "entries" not in new_wallet:
            raise Exception("Error when creating wallet")

        pubkey = skycoin.cipher_PubKey()
        seckey = skycoin.cipher_SecKey()
        error = skycoin.SKY_cipher_GenerateDeterministicKeyPair(
                seed.encode(), pubkey, seckey)
        if error != 0:
            raise Exception("No response when creating private and public keys for wallet")

        return {
            "privateKey": binascii.hexlify(bytearray(seckey.toStr())).decode('ascii'),
            "publicAddress": new_wallet["entries"][0]["address"],
            "addressContext": new_wallet['meta']['filename']
        }


    def form_url(self, base, path):
        """
        Conform the full URL from base URL and path
        """

        if path[0] != '/':
            path = '/' + path

        if base[len(base) - 1] == '/':
            base = base[0:len(base) - 1]

        url = base + path

        return url
