import unittest
import os
from exchange_app import app
from exchange_app.settings import app_config
import json
import skycoin
import binascii
import urllib.request
import time

LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL = "http://localhost:6421/"

class LiveTestCase(unittest.TestCase):

    def setUp(self):
        self.defaultSkycoinNodeUrl = app_config.SKYCOIN_NODE_URL
        app_config.SKYCOIN_NODE_URL = LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL
        self.app = app.test_client()
        #Wait for service to finish checking database (too big)
        time.sleep(10)
        self.wallets = self._createTestWallets()
        self.addressWithBalance = ""
        self.walletWithBalance = ""

        self.findAddressWithBalance()

    def tearDown(self):
        app_config.SKYCOIN_NODE_URL = self.defaultSkycoinNodeUrl

    def findAddressWithBalance(self):
        addresses = []
        for wallet in self.wallets:
            addresses.append(wallet["publicAddress"])
        values = {"addrs": ",".join(addresses)}
        balances = app.lykke_session.get(self.form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/balance"), params=values)
        if not balances.json:
            raise Exception("Error when getting wallet balances")

        response = balances.json()
        if "error" in response:
            raise Exception(response["error"]["message"])
        keys = response["addresses"].keys()
        self.addressWithBalance = ""
        for key in keys:
            coins = response["addresses"][key]["confirmed"]["coins"]
            if coins > 0:
                self.addressWithBalance = key
        assert self.addressWithBalance != "", "No wallet with balance " + str(response)

    def test_transaction(self):
        sourceAddress = self.addressWithBalance
        destAddress = ""
        for wallet in self.wallets:
            if self.addressWithBalance != wallet["publicAddress"]:
                destAddress = wallet["publicAddress"]


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
        wallets = []
        for seed in r["seeds"]:
            wallet = self._createWalletFromSeed(seed)
            wallets.append(wallet)
        return wallets


    def _createWalletFromSeed(self, seed):
        # generate CSRF token
        CSRF_token = app.lykke_session.get(self.form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/csrf")).json()

        if not CSRF_token or "csrf_token" not in CSRF_token:
            assert False, "Error requesting token from"
            #return {"status": 500, "error": "Unknown server error"}
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
