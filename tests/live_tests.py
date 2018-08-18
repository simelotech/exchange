import unittest
import os
from exchange_app import app
from exchange_app.settings import app_config
import json
import skycoin
import binascii
import urllib.request
import urllib.parse
import time
import logging
import codecs
import ssl

LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL = "https://skyapi.simelo.tech:6420/"

class LiveTestCase(unittest.TestCase):
    wallets = False
    serverUp = False

    def setUp(self):
        logging.debug("setup started")
        ssl._create_default_https_context = ssl._create_unverified_context
        self.defaultSkycoinNodeUrl = app_config.SKYCOIN_NODE_URL
        app_config.SKYCOIN_NODE_URL = LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL
        self.app = app.test_client()
        LiveTestCase.wallets = self._getTestWallets()
        self.addressWithBalance = "2JvBi6BgCsZAzvbhCna4WTfD4FATCPwp2f1"
        self.destinationAddress = "22TdufeUbAehE7ZnLuBUaTkacQHAFtCVnw2"
        self.destinationAddress2 = "jL6tDHrNg87BjxTQLqLqHFat987NgdeUMc"
        logging.debug("setup finished")
        #self.pickAddresses()


    def tearDown(self):
        pass
        #app_config.SKYCOIN_NODE_URL = self.defaultSkycoinNodeUrl

    def pickAddresses(self):
        values = {"addrs": ",".join(self.wallets.keys())}
        balances = app.lykke_session.get(self.form_url(app_config.SKYCOIN_NODE_URL, "/api/v1/balance"), params=values)
        if not balances.json:
            raise Exception("Error when getting wallet balances")

        response = balances.json()
        if "error" in response:
            raise Exception(response["error"]["message"])
        raise Exception(str(response))

    def _getBalanceForAddresses(self, addresses):
        logging.debug("Calling skycoin to get balances")
        data = {"addrs": ",".join(addresses)}
        data = urllib.parse.urlencode(data)
        balances = self.makeHttpRequest("api/v1/balance?"+data)
        if not balances:
            raise Exception("Error when getting wallet balances")
        if "error" in balances:
            raise Exception(balances["error"]["message"])
        result = {}
        for address in addresses:
            result[address] = balances["addresses"][address]["confirmed"]["coins"]
        return result

    def _transferSKY(self, sourceAddress, destAddresses, amounts, operationId):
        assert len(destAddresses) > 0
        assert len(destAddresses) == len(amounts)
        sourceWallet = self.wallets[sourceAddress]["addressContext"]
        privateKey = self.wallets[sourceAddress]["privateKey"]

        transaction_context = ""

        if len(destAddresses) == 1:
            testTx = {
                'operationID' : operationId,
                'fromAddress' : sourceAddress,
                'fromAddressContext' : sourceWallet,
                'toAddress' : destAddresses[0],
                'assetId' : 'SKY',
                'amount' : str(amounts[0]), #1000 droplet
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
        else:
            outputs = []
            i = 0
            for address in destAddresses:
                output = {
                    "toAddress" : address,
                    "amount" : str(amounts[i]) #1000 droplet
                }
                i += 1
                outputs.append(output)
            testTx = {
                'operationID' : operationId,
                'fromAddress' : sourceAddress,
                'fromAddressContext' : sourceWallet,
                'outputs' : outputs,
                'assetId' : 'SKY'
            }
            response = self.app.post(
                '/v1/api/transactions/many-outputs',
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
        hashHex = str(hashHex)
        if hashHex.startswith("b\'"):
            hashHex = hashHex[2:len(hashHex)-1]

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
        while tries > 0 and not confirmed:
            try:
                response = app.lykke_session.get(self.form_url(app_config.SKYCOIN_NODE_URL,
                    "/api/v1/transaction"),
                    params={"txid": hashHex})
                if response.status_code == 200:
                    json_response = response.json()
                    if not json_response:
                        raise Exception("Invalid response from /api/v1/transaction. No response")
                    logging.debug("Response from /api/v1/transaction: {}".format(json_response))
                    if json_response['txn']['txid'].lower() != hashHex.lower():
                        raise Exception("Received transaction info for the wrong transaction." + \
                            " {} != {}".format(json_response['txn']['txid'], hashHex))
                    confirmed = json_response["status"]["confirmed"]
                    logging.debug("Confirmed result: {}".format(confirmed))
                    if confirmed:
                        break
                if not confirmed:
                    logging.debug("Error getting transaction status or transaction not confirmed")
            except Exception as e:
                logging.debug("Error when checking transaction status. Error: {}".format(str(e)) )
            finally:
                tries -= 1
                if not confirmed:
                    time.sleep(timeOut)

    def test_transaction_single(self):
        sourceAddress = self.addressWithBalance
        destAddress = self.destinationAddress
        previousBalance = self._getBalanceForAddresses([sourceAddress, destAddress])
        self._transferSKY(sourceAddress, [destAddress], [1000], '4324432444332') #just some operation id
        newBalance = self._getBalanceForAddresses([sourceAddress, destAddress])
        self._transferSKY(destAddress, [sourceAddress], [1000], '4324432444333')
        backBalance = self._getBalanceForAddresses([sourceAddress, destAddress])

        self.assertEqual(previousBalance[sourceAddress],
            newBalance[sourceAddress] + 1000,
            "Address {0} should have lost 1000 droplets".format(sourceAddress))
        self.assertEqual(previousBalance[destAddress],
            newBalance[destAddress] - 1000,
            "Address {0} should have gained 1000 droplets".format(destAddress))
        self.assertEqual(previousBalance[sourceAddress],
            backBalance[sourceAddress],
            "Address {0} should have regained 1000 droplets".format(sourceAddress))
        self.assertEqual(previousBalance[destAddress],
            backBalance[destAddress],
            "Address {0} should have returned 1000 droplets".format(destAddress))

    def test_transaction_many_outputs(self):
        logging.debug("Test transaction many outputs")
        sourceAddress = self.addressWithBalance
        destAddress = self.destinationAddress
        destAddress2 = self.destinationAddress2
        previousBalance = self._getBalanceForAddresses([sourceAddress, destAddress, destAddress2])
        self._transferSKY(sourceAddress, [destAddress,destAddress2], [1000,1000], '1324432444332') #just some operation id
        newBalance = self._getBalanceForAddresses([sourceAddress, destAddress, destAddress2])
        self._transferSKY(destAddress, [sourceAddress], [1000], '1324432444333')
        self._transferSKY(destAddress2, [sourceAddress], [1000], '1324432444331')
        backBalance = self._getBalanceForAddresses([sourceAddress, destAddress, destAddress2])

        self.assertEqual(previousBalance[sourceAddress],
            newBalance[sourceAddress] + 2000,
            "Address {0} should have lost 2000 droplets".format(sourceAddress))
        self.assertEqual(previousBalance[destAddress],
            newBalance[destAddress] - 1000,
            "Address {0} should have gained 1000 droplets".format(destAddress))
        self.assertEqual(previousBalance[destAddress2],
            newBalance[destAddress2] - 1000,
            "Address {0} should have gained 1000 droplets".format(destAddress2))

        self.assertEqual(previousBalance[sourceAddress],
            backBalance[sourceAddress],
            "Address {0} should have regained 2000 droplets".format(sourceAddress))
        self.assertEqual(previousBalance[destAddress],
            backBalance[destAddress],
            "Address {0} should have returned 1000 droplets".format(destAddress))
        self.assertEqual(previousBalance[destAddress2],
            backBalance[destAddress2],
            "Address {0} should have returned 1000 droplets".format(destAddress2))


    def _getTestWallets(self):
        if LiveTestCase.wallets:
            return LiveTestCase.wallets
        seeds_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                *('data/skycoin/seeds.json'.split('/')))
        file = open(seeds_path, "r")
        text = file.read()
        r = json.loads(text)
        file.close()
        wallets = {}
        for seed in r["seeds"]:
            pubkey = skycoin.cipher_PubKey()
            seckey = skycoin.cipher_SecKey()
            error = skycoin.SKY_cipher_GenerateDeterministicKeyPair(
                    seed.encode(), pubkey, seckey)
            if error != 0:
                raise Exception("Error when creating private and public keys for wallet")

            wallet = {
                "seed" : seed,
                "privateKey": binascii.hexlify(bytearray(seckey.toStr())).decode('ascii'),
                "publicKey": binascii.hexlify(bytearray(pubkey.toStr())).decode('ascii')
            }
            wallets[wallet["publicKey"]] = wallet
        wallets = self._matchServerWallets(wallets)
        wallets = self._createMissingWallets(wallets)
        return wallets

    def _createMissingWallets(self, wallets):
        i = 0
        newWallets = {}
        for key in wallets.keys():
            wallet = wallets[key]
            if not "addressContext" in wallet:
                i += 1
                newWallet = self._createWalletFromSeed(wallet["seed"],
                    "testwallet" + str(i))
                wallet["addressContext"] = newWallet["addressContext"]
                wallet["publicAddress"] = newWallet["publicAddress"]
                assert wallet["privateKey"] == newWallet["privateKey"], "{} != {}".format(wallet["privateKey"], newWallet["privateKey"])
                assert wallet["publicKey"] == newWallet["publicKey"], "{} != {}".format(wallet["publicKey"], newWallet["publicKey"])
            newWallets[wallet["publicAddress"]] = wallet
        return newWallets

    def _matchServerWallets(self, wallets):
        serverWallets = self.makeHttpRequest( "api/v1/wallets" )
        if serverWallets is None:
            raise Exception("No response when getting wallets")
        matched = 0
        for wallet in serverWallets:
            walletName = wallet["meta"]["filename"]
            for entry in wallet["entries"]:
                pubkey = entry["public_key"]
                if pubkey in wallets:
                    wallets[pubkey]["addressContext"] = walletName
                    wallets[pubkey]["publicAddress"] = entry["address"]
                    matched += 1
                    break
            if matched == len(wallets):
                break
        return wallets


    def _createTestWallets(self):
        if LiveTestCase.wallets:
            return LiveTestCase.wallets
        seeds_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                *('data/skycoin/seeds.json'.split('/')))
        file = open(seeds_path, "r")
        text = file.read()
        r = json.loads(text)
        file.close()
        wallets = {}
        i = 0
        for seed in r["seeds"]:
            wallet = self._createWalletFromSeed(seed, "testwallet{}".format(i))
            wallets[wallet["publicAddress"]] = wallet
            i += 1
        return wallets

    def _getCSRFToken(self):
        # generate CSRF token
        tries = 1
        if not LiveTestCase.serverUp:
            tries = 5
        timeOut = 5
        CSRF_token = False
        i = 1
        while tries > 0:
            print("Connecting to skycoin node. Try: {}".format(i))
            logging.debug("Connecting to skycoin node. Try: {}".format(i))
            i += 1
            try:
                CSRF_token = self.makeHttpRequest("api/v1/csrf")
                if CSRF_token and "csrf_token" in CSRF_token:
                    break
            except Exception as e:
                logging.debug("Error requesting csrf token. Error: {}".format(e))
                time.sleep(timeOut)
            tries -= 1
        if not CSRF_token or "csrf_token" not in CSRF_token:
            assert False, "Error requesting token"
        LiveTestCase.serverUp = True
        return CSRF_token

    def _createWalletFromSeed(self, seed, label):
        CSRF_token = self._getCSRFToken()
        logging.debug("Got csrf token: {}".format(CSRF_token['csrf_token']))
        logging.debug("Calling skycoin to create wallet with seed")
        # create the wallet from seed
        data = {"seed": seed, "label": label, "scan": "5"}
        headers = {'X-CSRF-Token': CSRF_token['csrf_token']}
        new_wallet = self.makeHttpRequest("api/v1/wallet/create", data, headers)

        if not new_wallet:
            raise Exception("No response when creating wallet")

        if not new_wallet or "entries" not in new_wallet:
            raise Exception("Error when creating wallet")

        pubkey = skycoin.cipher_PubKey()
        seckey = skycoin.cipher_SecKey()
        error = skycoin.SKY_cipher_GenerateDeterministicKeyPair(
                seed.encode(), pubkey, seckey)
        if error != 0:
            raise Exception("No response when creating private and public keys for wallet")

        result = {
            "privateKey": binascii.hexlify(bytearray(seckey.toStr())).decode('ascii'),
            "publicKey": binascii.hexlify(bytearray(pubkey.toStr())).decode('ascii'),
            "publicAddress": new_wallet["entries"][0]["address"],
            "addressContext": new_wallet['meta']['filename']
        }
        logging.debug("Wallet created {}".format(str(result)))
        return result

    def makeHttpRequest(self, url, data = None, headers = None):
        if data:
            data = urllib.parse.urlencode(data)
            data = data.encode()
        logging.debug("Making request to {} with data {}".format(url, data))
        request = urllib.request.Request(app_config.SKYCOIN_NODE_URL + url)
        if headers:
            for key in headers.keys():
                request.add_header(key, headers[key])
        response = urllib.request.urlopen(request, data)
        if not response:
            logging.debug("Error. No response from {}".format(url))
            raise Exception("Error. No response from {}".format(url))
        result = str(response.read().replace(b'\n', b''))
        if result.startswith("b\'"):
            result = result[2:len(result)-1]
        logging.debug("Result from request: " + str(result))
        return json.loads(result)

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
