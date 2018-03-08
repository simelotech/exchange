import logging

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    TESTING = False
    PRODUCTION = False

    SECRET_KEY = '1!qaz2@wsx3#edc$4rfv'
    WTF_CSRF_SECRET_KEY = '1!qaz2@wsx3#edc$4rfv'
    SITE_NAME = ''
    LOG_LEVEL = logging.DEBUG
    SERVER_NAME = 'localhost:5000'
    #: Database
    MONGO_DBNAME = 'LYKKE'
    MONGO_HOST = '192.168.56.101'
    MONGO_PORT = 27017
    #MONGOALCHEMY_USER = ''
    #MONGOALCHEMY_PASSWORD = ''
    #: Redis
    REDIS_URL = 'redis://192.168.56.101:6379/0'


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
