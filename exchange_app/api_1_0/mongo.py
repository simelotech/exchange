from .. import db
#from flask_mongoalchemy import MongoAlchemy
from mongoalchemy.document import Document, Index, DocumentField
import logging

#used to connect to mongodb directly by driver. No need if Mongoalchemy is used
from pymongo import MongoClient
from .. import app


#Defining classes for wallet
class Entry (db.Document):
    address = db.StringField()
    public_key = db.StringField()
    secret_key = db.StringField()
    
class Meta (db.Document):
    coin = db.StringField()
    filename = db.StringField()
    label = db.StringField()
    lastSeed = db.StringField()
    seed = db.StringField()
    tm = db.StringField()
    type = db.StringField()
    version = db.StringField()
    
class Wallet (db.Document):
    entries = db.AnythingField([])
    meta = db.DocumentField(Meta)
    

def mongo_store_wallet(document):
    #TODO: Use mongoalchemy
    
    client = MongoClient(app.config["MONGOALCHEMY_SERVER"], app.config["MONGOALCHEMY_PORT"])
    database = client[app.config["MONGOALCHEMY_DATABASE"]]
    wallets_collection = database.wallets  #this colection will store all deposit wallets generated in blockchain
    
    if app.config['DEBUG']:
        logging.debug("Saving to MongoDB")
        logging.debug("Server %s", app.config["MONGOALCHEMY_SERVER"])
        logging.debug("Port %d", app.config["MONGOALCHEMY_PORT"])
        logging.debug("Database %s", app.config["MONGOALCHEMY_DATABASE"])
        logging.debug("Document %s", document)
        
    
    
    id = wallets_collection.insert(document)
    
    
def add_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    #TODO: Use mongoalchemy
    
    client = MongoClient(app.config["MONGOALCHEMY_SERVER"], app.config["MONGOALCHEMY_PORT"])
    database = client[app.config["MONGOALCHEMY_DATABASE"]]
    wallets_collection = database.observation  #this colection will store all wallets addresses for balance observation
    
    if app.config['DEBUG']:
        logging.debug("Saving address to observation list")
        logging.debug("Server %s", app.config["MONGOALCHEMY_SERVER"])
        logging.debug("Port %d", app.config["MONGOALCHEMY_PORT"])
        logging.debug("Database %s", app.config["MONGOALCHEMY_DATABASE"])
        logging.debug("address %s", address)
    
    id = wallets_collection.insert({'address':address})
    
    return id
    
def delete_address_observation(address):
    """
    Add the specified address to observation list and return the mongo document id
    """
    #TODO: Use mongoalchemy
    
    client = MongoClient(app.config["MONGOALCHEMY_SERVER"], app.config["MONGOALCHEMY_PORT"])
    database = client[app.config["MONGOALCHEMY_DATABASE"]]
    wallets_collection = database.observation  #this colection will store all wallets addresses for balance observation
    
    if app.config['DEBUG']:
        logging.debug("Deleting address from observation list")
        logging.debug("Server %s", app.config["MONGOALCHEMY_SERVER"])
        logging.debug("Port %d", app.config["MONGOALCHEMY_PORT"])
        logging.debug("Database %s", app.config["MONGOALCHEMY_DATABASE"])
        logging.debug("address %s", address)
    
    id = wallets_collection.remove({'address':address})
    
    return id
