import logging

def validate_transaction_single(json):
    if not json:
        logging.debug('/api/transactions/single - No json data')
        return False, "Input format error"
    params = {'operationID', 'fromAddress', 'fromAddressContext',
            'toAddress', 'assetId', 'amount', 'includeFee'}
    if all(x not in params for x in json):
        logging.debug('/api/transactions/single - Missing parameters')
        return False, "Input format error"
    try:
        amount = int(json['amount'])
    except:
        logging.debug('/api/transactions/single - Error while parsing amount')
        return False, "Amount is not an integer"
    if amount <= 0:
        logging.debug('/api/transactions/single - Amount is zero')
        return False, "Amount is zero"
    if json['assetId'] != 'SKY':
        logging.debug('/api/transactions/single - Asset id must be sky')
        return False, "Only coin is sky"
    return True, ""

def validate_sign_transaction_single(json):
    if not json:
        logging.debug('sign_transaction - No json data')
        return False, "Input format error"
    params = {'operationID', 'fromAddress', 'fromAddressContext',
            'toAddress', 'assetId', 'amount', 'includeFee'}
    if all(x not in params for x in json):
        logging.debug('sign_transaction - Missing parameters')
        return False, "Input format error"
    if json['assetId'] != 'SKY':
        logging.debug('sign_transaction - Asset id must be sky')
        return False, "Only coin is sky"
    return True, ""

def validate_transaction_broadcast(json):
    if not json:
        logging.debug('/api/transactions/broadcast - No json data')
        return False, 'Invalid Input Format'
    if "operationId" not in json:
        logging.debug('/api/transactions/broadcast - Missing parameters')
        return False, 'Invalid Input Parameters'
    if "signedTransaction" not in json:
        logging.debug('/api/transactions/broadcast - Missing parameters')
        return False, 'Invalid Input Parameters'
    return True, ""
