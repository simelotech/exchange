import logging
import os
from flask import Flask
from flask_redis import FlaskRedis
from flask_pymongo import PyMongo
import requests
import json

FLASK_APP_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__
)


# Lykke Settings
@app.before_first_request
def setup_lykke_settings():
    settings_url = os.getenv('SettingsUrl')
    data = {}
    if not settings_url:
        app.logger.error("Lykke Settings not in Enviroment")
        #: TODO What if Lykke settings are not loaded?
    if app.config['ENVIRONMENT'] == 'Dev' or app.config['ENVIRONMENT'] == 'Testing' and 'file' in settings_url.split('://'):
        app.logger.info("Loading Lykke Settings via {}".format(settings_url))
        with open(settings_url.split('file://')[1]) as f:
            data = json.load(f)
    if app.config['ENVIRONMENT'] == 'Production':
        app.logger.info("Loading Lykke Settings via {}".format(settings_url))
        r = requests.get(settings_url)
        data = r.json()
    app.config.update(data)


# Config
app.config.from_object('exchange_app.settings.app_config')
app.logger.info("Config: %s" % app.config['ENVIRONMENT'])

# Logging
logging.basicConfig(
    level=app.config['LOG_LEVEL'],
    format='%(asctime)s %(levelname)s: %(message)s '
           '[in %(pathname)s:%(lineno)d]',
    datefmt='%Y%m%d-%H:%M%p',
)

#: Session, Used for connection pooling requests to lykke api
app.lykke_session = requests.Session()

# Redis
redis_store = FlaskRedis(app, strict=False)

# MongoDB
mongo = PyMongo(app)

# Business Logic
from . import signservice
from .api_1_0 import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/v1/api')
