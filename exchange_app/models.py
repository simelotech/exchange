import logging
from exchange_app import mongo, app

def add_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
    if app.config['DEBUG']:
        logging.debug("Saving address to observation list")
        logging.debug("Server %s", app.config["MONGOALCHEMY_SERVER"])
        logging.debug("Port %d", app.config["MONGOALCHEMY_PORT"])
        logging.debug("Database %s", app.config["MONGOALCHEMY_DATABASE"])
        logging.debug("address %s", address)
    
    #If address not observed, insert it
    if not exists_address_observation(address):
        id = wallets_collection.insert({'address':address})
        return id
    else:
        return {"status" : 409, "error": "Specified address is already observed"} 

    
def delete_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
    if app.config['DEBUG']:
        logging.debug("Deleting address from observation list")
        logging.debug("Server %s", app.config["MONGOALCHEMY_SERVER"])
        logging.debug("Port %d", app.config["MONGOALCHEMY_PORT"])
        logging.debug("Database %s", app.config["MONGOALCHEMY_DATABASE"])
        logging.debug("address %s", address)
    
    #If address already observed, delete it
    if exists_address_observation(address):
        result = wallets_collection.remove({'address':address})
        return result
    else:
        return {"status" : 204, "error": "Specified address is not observed"} 
    
    
    

def get_address_list():
    """
    return addresses in observation list
    """

    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
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
