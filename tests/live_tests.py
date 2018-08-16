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
        self.destinationAddress = ""
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
            self.wallets[key]['balance'] = coins
        assert self.addressWithBalance != "", "No wallet with balance"
        for key in keys:
            if key != self.addressWithBalance:
                self.destinationAddress = key
        assert self.destinationAddress != "", "Couldn't find a destination address"


    def _transferSKY(self, sourceAddress, destAddress, operationId):
        sourceWallet = self.wallets[sourceAddress]["addressContext"]
        privateKey = self.wallets[sourceAddress]["privateKey"]

        testTx = {
            'operationID' : operationId,
            'fromAddress' : sourceAddress,
            'fromAddressContext' : sourceWallet,
            'toAddress' : destAddress,
            'assetId' : 'SKY',
            'amount' : '1000', #1000 droplet
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
        signedTransaction = json_response['signedTransaction']
        #Test deserializing back the signed transaction
        serialized = codecs.decode(json_response['signedTransaction'], 'hex')
        error, transaction_handle = skycoin.SKY_coin_TransactionDeserialize(serialized)
        self.assertEqual( error, 0, "Error deserializing signed transaction")
        self.assertNotEqual(transaction_handle, 0, "Invalid handle returned from SKY_coin_TransactionDeserialize")
        hash = skycoin.cipher_SHA256()
        error = skycoin.SKY_coin_Transaction_Hash(transaction_handle, hash)
        skycoin.SKY_handle_close(transaction_handle)
        self.assertEqual(error, 0, "Error getting transaction hash")

        #Get transaction hash to check for confirmation
        error, hashHex = skycoin.SKY_cipher_SHA256_Hex(hash)
        self.assertEqual(error, 0, "Error converting hash to hex")

        #Test transaction broadcast
        data = {
            "operationId" : operationId,
            "signedTransaction" : signedTransaction,
        }
        response = self.app.post(
            '/v1/api/transactions/broadcast',
            data = json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


        timeOut = 5
        tries = 10
        confirmed = False
        while tries > 10 and not confirmed:
            try:
                response = app.lykke_session.get(form_url(app_config.SKYCOIN_NODE_URL,
                    "/api/v1/transaction"),
                    params={"txid": hashHex})
                if response.status_code == 200:
                    json_response = json.loads(response.get_data(as_text=True))
                    if not json_response:
                        raise Exception("Invalid response from /api/v1/transaction. No response")
                    logging.debug("Response from /api/v1/transaction: {}".format(json_response))
                    if lower(json_response['txn']['txid']) != lower(hashHex):
                        raise Exception("Received transaction info for the wrong transaction." + \
                            " {} != {}".format(json_response['txn']['txid'], hashHex))
                    confirmed = json_response["status"]["confirmed"]
                    loggin.debug("Confirmed result: {}".format(confirmed))
                if not confirmed:
                    time.sleep(timeOut)
                    tries -= 1
            except Exception as e:
                loggin.debug("Error when checking transaction status. Error: {}".format(str(e)) )


    def test_transaction_single(self):
        sourceAddress = self.addressWithBalance
        #save previous balance to check after transaction is confirmed
        previous_balance = self.wallets[sourceAddress]['balance']
        destAddress = self.destinationAddress
        self._transferSKY(sourceAddress, destAddress, '4324432444332') #just some operation id
        self._transferSKY(destAddress, sourceAddress, '4324432444333')

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
        timeOut = 7
        CSRF_token = False
        while tries > 0:
            try:
                CSRF_token = app.lykke_session.get(self.form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/csrf")).json()
                if CSRF_token and "csrf_token" in CSRF_token:
                    break
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
            "publicKey": binascii.hexlify(bytearray(pubkey.toStr())).decode('ascii'),
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
