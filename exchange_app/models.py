import logging
from flask_pymongo.wrappers import Collection
from exchange_app import mongo, app


def store_wallet(document):
    """
    Add the wallet info, return None
    """
    wallet = mongo.db.wallets
    wallet.insert(document)
    if app.config['DEBUG']:
        logging.debug("Saving to MongoDB")
        logging.debug("Server %s", app.config["MONGO_HOST"])
        logging.debug("Port %d", app.config["MONGO_PORT"])
        logging.debug("Database %s", app.config["MONGO_DBNAME"])
        logging.debug("Document %s", document)


def add_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    wallets_collection = mongo.db.observation
    if app.config['DEBUG']:
        logging.debug("Saving address to observation list")
        logging.debug("Server %s", app.config["MONGO_HOST"])
        logging.debug("Port %d", app.config["MONGO_PORT"])
        logging.debug("Database %s", app.config["MONGO_DBNAME"])
        logging.debug("address %s", address)
    id = wallets_collection.insert({'address': address})
    return id


def delete_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    wallets_collection = mongo.db.observation
    if app.config['DEBUG']:
        logging.debug("Deleting address from observation list")
        logging.debug("Server %s", app.config["MONGO_HOST"])
        logging.debug("Port %d", app.config["MONGO_PORT"])
        logging.debug("Database %s", app.config["MONGO_DBNAME"])
        logging.debug("address %s", address)
    id = wallets_collection.remove({'address': address})
    return id


def get_address_list():
    """
    return addresses in observation list
    """
    wallets_collection = mongo.db.observation
    result = wallets_collection.find()
    addresses = []
    for addr in result:
        addresses.append(addr['address'])
    return addresses


def exists_address_observation(address):
    """
    return addresses in observation list
    """
    wallets_collection = mongo.db.observation
    result = wallets_collection.find_one({'address': address})
    if result:
        return True
    else:
        return False
