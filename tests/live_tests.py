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
#LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL = "http://127.0.0.1:6421/"
SYNCHRONIZATION_SERVER = "http://107.173.160.237:8080/"  #107.173.160.237

class LiveTestCase(unittest.TestCase):
    serverUp = False

    def setUp(self):
        logging.debug("setup started")
        ssl._create_default_https_context = ssl._create_unverified_context
        self.defaultSkycoinNodeUrl = app_config.SKYCOIN_NODE_URL
        app_config.SKYCOIN_NODE_URL = LIVE_TRANSACTIONS_TEST_SKYCOIN_NODE_URL
        self.app = app.test_client()
        self._getCSRFToken()
        self.wallets = self._getTestWallets()
        self.mainAddress = "2JvBi6BgCsZAzvbhCna4WTfD4FATCPwp2f1"
        self.lockIndexes = self._getLockIndexes(3)
        logging.debug("Lock indexes: {}".format(self.lockIndexes))
        addresses = self._generateNewAddresses(3, self.lockIndexes)
        self.assertEqual(len(addresses), 3,
            "3 new addresses should have been created")
        self.addressWithBalance = addresses[0]
        self.destinationAddress = addresses[1]
        self.destinationAddress2 = addresses[2]
        logging.debug("setup finished")

    def tearDown(self):
        self._unlockIndexes(self.lockIndexes)
        balance = self._getBalanceForAddresses([self.mainAddress,
            self.addressWithBalance])
        logging.debug("Balance at tearDown: {}".format(balance))

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

    def _pickOutputFromAddress(self, address, amount, minimum = 32):
        #Pick the output with less coin hours
        #but with at least 10 to be able to
        #return SKY to original address
        data = urllib.parse.urlencode({"addrs" : address})
        outputs = self.makeHttpRequest("api/v1/outputs?" + data)
        min_hours = 1000000000
        hash = ''
        for output in outputs["head_outputs"]:
            hours = output['hours']
            coins = float(output['coins'])
            if coins >= amount + 0.001 and hours >= minimum and hours < min_hours:
                min_hours = hours
                hash = output['hash']
        assert hash != '', "No outputs to spend"
        logging.debug("Picked output {} with {} hours".format(hash, min_hours))
        return hash

    def _transferSKYEx(self, sourceAddress, destAddress, amount, output):
        amount = float(amount) / 1000000 #Convert to droplets
        logging.debug("******Transferring from {} to {}, amount {}".format( \
            sourceAddress, destAddress, amount))
        sourceWallet = self.wallets[sourceAddress]["addressContext"]
        privateKey = self.wallets[sourceAddress]["privateKey"]
        tx = {
            "hours_selection": {
                "type": "auto",
                "mode": "share",
                "share_factor": "0.5"
            },
            "wallet": {
                "id": sourceWallet
            },
            "to" : [{
                "address" : destAddress,
                "coins" : "{:f}".format(amount)
            }]
        }
        if output:
            tx["wallet"]["unspents"] = [output]
        else:
            tx["wallet"]["addresses"] = [sourceAddress]
        CSRF_token = self._getCSRFToken()
        logging.debug("Calling skycoin to create new transaction")
        response = app.lykke_session.post(form_url(app_config.SKYCOIN_NODE_URL,
                '/api/v1/wallet/transaction'),
                data=json.dumps(tx),
                headers={'X-CSRF-Token': CSRF_token['csrf_token'],
                "Content-Type" : "application/json"},
                verify = app_config.VERIFY_SSL)
        if response.status_code != 200:
            raise Exception("Error creating transaction: {}".format(response.text))
        transaction = response.json()
        if not transaction:
            logging.debug("Error creating transaction")
            raise Exception("Error creating transaction")
        if "error" in transaction:
            msg = "Error creating transaction: {} : {}".format(\
                transaction["error"]["code"],
                transaction["error"]["message"])
            raise Exception(msg)
        assert "encoded_transaction" in transaction, "Invalid transaction"
        encoded_transaction = transaction["encoded_transaction"]
        CSRF_token = self._getCSRFToken()
        data = {"rawtx" : encoded_transaction}
        logging.debug("Calling skycoin to broadcast transaction")
        response = app.lykke_session.post(form_url(app_config.SKYCOIN_NODE_URL,
                '/api/v1/injectTransaction'),
                data=json.dumps(data),
                headers={'X-CSRF-Token': CSRF_token['csrf_token'],
                "Content-Type" : "application/json"},
                verify = app_config.VERIFY_SSL)
        if response.status_code != 200:
            raise Exception("Error broadcasting transaction: {}".format(response.text))
        confirmed = self._waitForTransactionConfirmation(encoded_transaction)
        if not confirmed:
            raise Exception("Transaction not confirmed")


    def _waitForTransactionConfirmation(self, encoded_transaction):
        serialized = codecs.decode(encoded_transaction, 'hex')
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
        timeOut = 5
        tries = 10
        confirmed = False
        while tries > 0 and not confirmed:
            try:
                params={"txid": hashHex}
                json_response = self.makeHttpRequest("api/v1/transaction?" + urllib.parse.urlencode(params))
                if json_response:
                    if json_response['txn']['txid'].lower() != hashHex.lower():
                        raise Exception("Received transaction info for the wrong transaction." + \
                            " {} != {}".format(json_response['txn']['txid'], hashHex))
                    confirmed = json_response["status"]["confirmed"]
                    logging.debug("Confirmed result: {}".format(confirmed))
                    if confirmed:
                        break
                else:
                    raise Exception("Invalid response from /api/v1/transaction. No response")
                if not confirmed:
                    logging.debug("Error getting transaction status or transaction not confirmed")
            except Exception as e:
                logging.debug("Error when checking transaction status. Error: {}".format(str(e)) )
            finally:
                tries -= 1
                if not confirmed:
                    time.sleep(timeOut)
        return confirmed


    def _transferSKY(self, sourceAddress, destAddresses, amounts, operationId):
        logging.debug("******Transferring from {} to {}, amount {}, operation {}".format( \
            sourceAddress, str(destAddresses), str(amounts),
            operationId))
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

        #Transaction sign
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

        #Transaction broadcast
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

        confirmed = self._waitForTransactionConfirmation(signedTransaction)
        if not confirmed:
            raise Exception("Error, transaction not confirmed")


    def _getSomeSkyForTest(self, amount, minCoinHours):
        #Pick an output with enough coin hours that will allow
        #subsequent transfers
        output = self._pickOutputFromAddress(self.mainAddress, amount / 10e6, minCoinHours)
        balance = self._getBalanceForAddresses([self.mainAddress,
            self.addressWithBalance])
        logging.debug("Balance: {}".format(balance))
        self._transferSKYEx(self.mainAddress,
            self.addressWithBalance, amount, output)
        balance = self._getBalanceForAddresses([self.mainAddress,
            self.addressWithBalance])
        logging.debug("Balance: {}".format(balance))

    def _printOutputsForAddress(self, address):
        result = self.makeHttpRequest("api/v1/outputs?addrs=" + address)
        logging.debug("Outputs for address {}: {}".format( address, str(result)))

    def test_transaction_single(self):
        transferredTo = ''
        #Requires at least 16 coin hours to make 2 more transactions
        self._getSomeSkyForTest(amount = 1000, minCoinHours = 16)
        sourceAddress = self.addressWithBalance
        destAddress = self.destinationAddress
        transferredTo = self.addressWithBalance
        previousBalance = self._getBalanceForAddresses([sourceAddress,
                            destAddress])
        logging.debug("Balance: {}".format(previousBalance))
        self._printOutputsForAddress(destAddress)
        self._transferSKY(sourceAddress, [destAddress], [1000],
                '4324432444332') #just some operation id
        self._printOutputsForAddress(destAddress)
        transferredTo = destAddress
        newBalance = self._getBalanceForAddresses([sourceAddress,
                destAddress])
        logging.debug("Balance: {}".format(newBalance))
        if transferredTo != '':
            self._transferSKYEx(transferredTo,
                self.mainAddress, 1000, False)
        self.assertEqual(previousBalance[sourceAddress],
            newBalance[sourceAddress] + 1000,
            "Address {0} should have lost 1000 droplets".format(sourceAddress))
        self.assertEqual(previousBalance[destAddress],
            newBalance[destAddress] - 1000,
            "Address {0} should have gained 1000 droplets".format(destAddress))

    def test_transaction_many_outputs(self):
        logging.debug("Test transaction many outputs")
        #Requires at least 32 coin hours to make one many outputs
        #transaction and one single output transaction
        self._printOutputsForAddress(self.addressWithBalance)
        self._getSomeSkyForTest(amount = 2000, minCoinHours = 32)
        self._printOutputsForAddress(self.addressWithBalance)
        sourceAddress = self.addressWithBalance
        destAddress = self.destinationAddress
        destAddress2 = self.destinationAddress2

        previousBalance = self._getBalanceForAddresses([sourceAddress,
                            destAddress, destAddress2])
        logging.debug("Balance: {}".format(previousBalance))
        self._printOutputsForAddress(destAddress)
        self._printOutputsForAddress(destAddress2)
        self._transferSKY(sourceAddress, [destAddress, destAddress2],
                [1000, 1000], '555555555') #just some operation id
        self._printOutputsForAddress(destAddress)
        self._printOutputsForAddress(destAddress2)
        newBalance = self._getBalanceForAddresses([sourceAddress,
                destAddress, destAddress2])
        self.assertEqual(previousBalance[sourceAddress],
            newBalance[sourceAddress] + 2000,
            "Address {0} should have lost 2000 droplets".format(sourceAddress))
        self.assertEqual(previousBalance[destAddress],
            newBalance[destAddress] - 1000,
            "Address {0} should have gained 1000 droplets".format(destAddress))
        self.assertEqual(previousBalance[destAddress2],
            newBalance[destAddress2] - 1000,
            "Address {0} should have gained 1000 droplets".format(destAddress2))
        self._transferSKYEx(destAddress,
            self.mainAddress, 1000, False)
        self._transferSKYEx(destAddress2,
            self.mainAddress, 1000, False)

    def _getTestWallets(self):
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
                #new created wallet should have 1 address
                wallet["entries_count"] = 1
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
                    wallets[pubkey]["entries_count"] = len(wallet["entries"])
                    matched += 1
                    break
            if matched == len(wallets):
                break
        return wallets

    def _getCSRFToken(self):
        # generate CSRF token
        tries = 1
        if not LiveTestCase.serverUp:
            tries = 50
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
        logging.debug("Wallet created {}".format(str(result["publicAddress"])))
        return result

    def _generateNewAddresses(self, n, indexes):
        addresses = []
        mainWallet = self.wallets[self.mainAddress]
        wallet_entries = mainWallet["entries_count"]
        maxIndex = 0
        for index in indexes:
            if index > maxIndex:
                maxIndex = index
        if maxIndex + 1 > wallet_entries:
            #Generate addresses until we reach the indexes
            newAddressesCount = maxIndex + 1 - wallet_entries
            newaddresses = self._createNewAddresses( newAddressesCount)
            logging.debug("New addresses created in skycoin: {}".format(newaddresses))
        addresses = []
        for index in indexes:
            wallet = self._getAddressByIndex(index)
            addresses.append(wallet["publicAddress"])
            self.wallets[wallet["publicAddress"]] = wallet
        return addresses

    def _createNewAddresses(self, n):
        mainWallet = self.wallets[self.mainAddress]
        CSRF_token = self._getCSRFToken()
        logging.debug("Calling skycoin to create new addresses")
        # create addresses in the wallet
        data = {"id": mainWallet["addressContext"], "num": n}
        headers = {'X-CSRF-Token': CSRF_token['csrf_token']}
        new_addresses = self.makeHttpRequest("api/v1/wallet/newAddress", data, headers)
        logging.debug("New addresses created: {}".format(str(new_addresses)))

    def _getAddressByIndex(self, index):
        addresses = []
        mainWallet = self.wallets[self.mainAddress]
        wallet_entries = mainWallet["entries_count"]
        logging.debug("Wallet with main address {} has {} addresses".format( \
            self.mainAddress, wallet_entries))
        seed = mainWallet["seed"]
        seed = seed.encode()
        pubkey = skycoin.cipher_PubKey()
        seckey = skycoin.cipher_SecKey()
        i = 0
        while i < index:
            error, new_seed = \
                skycoin.SKY_cipher_DeterministicKeyPairIterator(seed,
                pubkey, seckey)
            self.assertEqual(error, 0, "Error with SKY_cipher_DeterministicKeyPairIterator")
            seed = new_seed
            i += 1
        #Got the seed, lets generate
        error, new_seed = \
            skycoin.SKY_cipher_DeterministicKeyPairIterator(seed,
            pubkey, seckey)
        self.assertEqual(error, 0, "Error with SKY_cipher_DeterministicKeyPairIterator")
        address = skycoin.cipher__Address()
        err = skycoin.SKY_cipher_AddressFromPubKey(pubkey, address)
        self.assertEqual(error, 0, "Error creating address from pub key.")
        error, strAddress = skycoin.SKY_cipher_Address_String(address)
        self.assertEqual(error, 0, "Error with SKY_cipher_Address_String")
        strAddress = str(strAddress)
        if strAddress.startswith("b\'"):
            strAddress = strAddress[2:len(strAddress)-1]
        logging.debug("Address generated: {}".format(strAddress))
        newWallet = {
            "privateKey": binascii.hexlify(bytearray(seckey.toStr())).decode('ascii'),
            "publicKey": binascii.hexlify(bytearray(pubkey.toStr())).decode('ascii'),
            "publicAddress": strAddress,
            "addressContext": mainWallet["addressContext"]
        }
        return newWallet

    def _getLockIndexes(self, n):
        lockIndexes = self.makeHttpRequest("lock?n={}".format(n), None, None, SYNCHRONIZATION_SERVER)
        return lockIndexes["indexes"]

    def _unlockIndexes(self, indexes):
        logging.debug("Unlocking indexes: {}".format(indexes))
        data = {"n": ",".join(str(x) for x in indexes)}
        url = "free?" + urllib.parse.urlencode(data)
        result = self.makeHttpRequest(url, None, None, SYNCHRONIZATION_SERVER)

    def makeHttpRequest(self, url, data = None, headers = None, server = False):
        if not server:
            server = app_config.SKYCOIN_NODE_URL
        if data:
            data = urllib.parse.urlencode(data)
            data = data.encode()
        logging.debug("Making request to {}".format(url))
        request = urllib.request.Request(server + url)
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
        return json.loads(result)

def form_url(base, path):
    """
    Conform the full URL from base URL and path
    """

    if path[0] != '/':
        path = '/' + path

    if base[len(base) - 1] == '/':
        base = base[0:len(base) - 1]

    url = base + path

    return url


def get_url(path, values=""):
    """
    General GET function for blockchain
    """

    url = form_url(app_config.SKYCOIN_NODE_URL, path)

    # resp = requests.get(url, params = values)
    # response_data = resp.json()

    response_data = {"Called": "get_url()", "url": url, "values:": values}

    return response_data


def post_url(path, values=""):
    """
    General POST function for blockchain
    """

    url = form_url(app_config.SKYCOIN_NODE_URL, path)

    # resp = requests.post(url, data = values)
    # response_data = resp.json()

    response_data = {"Called": "post_url()", "url": url, "values:": values}

    return response_data

def get_transaction_context(tx):
	#TODO: Find a more ellegant way to create the context
	return json.dumps(tx)

def get_transaction_from_context(context):
    try:
        return json.loads(context)
    except:
        return False
