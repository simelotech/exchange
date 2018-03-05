import logging
from flask_pymongo.wrappers import Collection
from mongoalchemy.document import Document, Index, DocumentField
from exchange_app import mongo, app


def store_wallet(document):
    wallet = mongo.db.wallets
    wallet.insert(document)
    if app.config['DEBUG']:
        logging.debug("Saving to MongoDB")
        logging.debug("Server %s", app.config["MONGO_HOST"])
        logging.debug("Port %d", app.config["MONGO_HOST"])
        logging.debug("Database %s", app.config["MONGO_DBNAME"])
        logging.debug("Document %s", document)
