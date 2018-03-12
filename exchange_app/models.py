import logging
from exchange_app import mongo, app

def add_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
    
    #If address not observed, insert it
    if not exists_address_observation(address):
        id = wallets_collection.insert({'address':address})
        if isinstance(id, ObjectId):
            return id 
        else:
            return {"status": 500, "error": "Unknown server error"}
    else:
        return {"status" : 409, "error": "Specified address is already observed"} 

    
def delete_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    
    wallets_collection = mongo.db.observation  #this colection will store all wallets addresses for balance observation
        
    #If address already observed, delete it
    if exists_address_observation(address):
        result = wallets_collection.remove({'address':address})
        
        if not 'n' in result:
            return {"status": 500, "error": "Unknown server error"}
        if result['n'] == 0:
            return {"status": 500, "error": "Unknown server error"}
            
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

        
def exists_address_transfer_observation_to(address):
    """
    return addresses in observation list
    """
    wallets_collection = mongo.db.trans_obs_to
    result = wallets_collection.find_one({'address': address})
    if result:
        return True
    else:
        return False
        
def exists_address_transfer_observation_from(address):
    """
    return addresses in observation list
    """
    wallets_collection = mongo.db.trans_obs_from
    result = wallets_collection.find_one({'address': address})
    if result:
        return True
    else:
        return False
        
        

def add_transaction_observation_from_address(address):
    """
    Add the specified address to transaction observation list to it and return the mongo document id
    """
    
    wallets_collection = mongo.db.trans_obs_from  #this colection will store all wallets addresses for transaction observation from it
    
    #If address not observed, insert it
    if not exists_address_transfer_observation_from(address):
        id = wallets_collection.insert({'address':address})
        
        if isinstance(id, ObjectId):
            return id 
        else:
            return {"status": 500, "error": "Unknown server error"}
    else:
        return {"status" : 409, "error": "Specified address is already observed"} 

        
def add_transaction_observation_to_address(address):
    """
    Add the specified address to transaction observation list to it and return the mongo document id
    """
    
    wallets_collection = mongo.db.trans_obs_to  #this colection will store all wallets addresses for transaction observation from it
    
    #If address not observed, insert it
    if not exists_address_transfer_observation_to(address):
        id = wallets_collection.insert({'address':address})
        
        if isinstance(id, ObjectId):
            return id 
        else:
            return {"status": 500, "error": "Unknown server error"}
    else:
        return {"status" : 409, "error": "Specified address is already observed"} 
        