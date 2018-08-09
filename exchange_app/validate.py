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
        amount = int(request.json['amount'])
    except:
        logging.debug('/api/transactions/single - Error while parsing amount')
        return False, "Amount is not an integer"
    if json['assetId'] != 'sky':
        logging.debug('/api/transactions/single - Asset id must be sky')
        return False, "Only coin is sky"
    return True, ""

def validate_sign_transaction_single(json):
    if not json:
        logging.debug('/api/transactions/single - No json data')
        return False, "Input format error"
    params = {'operationID', 'fromAddress', 'fromAddressContext',
            'toAddress', 'assetId', 'amount', 'includeFee'}
    if all(x not in params for x in json):
        logging.debug('/api/transactions/single - Missing parameters')
        return False, "Input format error"
    if json['assetId'] != 'sky':
        logging.debug('/api/transactions/single - Asset id must be sky')
        return False, "Only coin is sky"
    return True, ""
