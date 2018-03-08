import logging
from exchange_app import mongo, app


<<<<<<< .merge_file_a12948
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
    
=======
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


>>>>>>> .merge_file_a06940
def delete_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
<<<<<<< .merge_file_a12948
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
    
    
=======
    wallets_collection = mongo.db.observation
    if app.config['DEBUG']:
        logging.debug("Deleting address from observation list")
        logging.debug("Server %s", app.config["MONGO_HOST"])
        logging.debug("Port %d", app.config["MONGO_PORT"])
        logging.debug("Database %s", app.config["MONGO_DBNAME"])
        logging.debug("address %s", address)
    id = wallets_collection.remove({'address': address})
    return id


>>>>>>> .merge_file_a06940
def get_address_list():
    """
    return addresses in observation list
    """
<<<<<<< .merge_file_a12948
    
    #TODO: Use mongoalchemy
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
    result = wallets_collection.find()
    
    addresses = []
    
    for addr in result:
        addresses.append(addr['address'])
    
    return addresses
=======
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
>>>>>>> .merge_file_a06940
