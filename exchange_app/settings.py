import logging

import os
import os.path

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    PRODUCTION = False

    SITE_NAME = ''
    LOG_LEVEL = logging.DEBUG
    SERVER_NAME = 'localhost:5000'
    #: REST API
    DEFAULT_LIST_LENGTH = 10
    #: Database
    MONGO_DBNAME = 'LYKKE'
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_URI = "mongodb://" + MONGO_HOST + ":" + str(MONGO_PORT) + "/" + MONGO_DBNAME
    #: Redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    #: Skycoin
    SECRET_KEY = '1!qaz2@wsx3#edc$4rfv'
    WTF_CSRF_SECRET_KEY = '1!qaz2@wsx3#edc$4rfv'
    SKYCOIN_NODE_URL = 'http://localhost:6420/'
    LIBSKYCOIN_PATH = os.path.join(*('exchange_app/libskycoin.so'.split('/')))
    SKYCOIN_WALLET_SHARED = False
    SKYCOIN_FIBER_ASSET = "SKY"
    SKYCOIN_FIBER_NAME = "Skycoin"
    #: Lykke
    LYKKE_API_VERSION = '1.3.0'


class ProductionConfig(Config):
    ENVIRONMENT = 'Production'
    PRODUCTION = True
    LOG_LEVEL = logging.INFO
    SERVER_NAME = ''


class DevelopmentConfig(Config):
    ENVIRONMENT = 'Dev'
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    ENVIRONMENT = 'Testing'
    DEBUG = False
    TESTING = True


environment = os.getenv('ENVIRONMENT', 'DEVELOPMENT').lower()

if environment == 'testing':
    app_config = TestingConfig()
elif environment == 'production':
    app_config = ProductionConfig()
else:
    app_config = DevelopmentConfig()
