import logging
from flask_pymongo.wrappers import Collection
from mongoalchemy.document import Document, Index, DocumentField
from exchange_app import mongo, app


def add_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    #TODO: Use mongoalchemy
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
    if app.config['DEBUG']:
        logging.debug("Saving address to observation list")
        logging.debug("Server %s", app.config["MONGOALCHEMY_SERVER"])
        logging.debug("Port %d", app.config["MONGOALCHEMY_PORT"])
        logging.debug("Database %s", app.config["MONGOALCHEMY_DATABASE"])
        logging.debug("address %s", address)
    
    #TODO: check for error when address is already observed
    id = wallets_collection.insert({'address':address})
    
    return id
    
def delete_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    #TODO: Use mongoalchemy
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
    if app.config['DEBUG']:
        logging.debug("Deleting address from observation list")
        logging.debug("Server %s", app.config["MONGOALCHEMY_SERVER"])
        logging.debug("Port %d", app.config["MONGOALCHEMY_PORT"])
        logging.debug("Database %s", app.config["MONGOALCHEMY_DATABASE"])
        logging.debug("address %s", address)
    
    #TODO: Check for error when address is not observed
    result = wallets_collection.remove({'address':address})
    
    return result
    
    
def get_address_list():
    """
    return addresses in observation list
    """
    
    #TODO: Use mongoalchemy
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
    result = wallets_collection.find()
    
    addresses = []
    
    for addr in result:
        addresses.append(addr['address'])
    
    return addresses