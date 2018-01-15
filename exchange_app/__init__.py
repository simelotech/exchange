import logging
import os
from flask import Flask
from flask_cache import Cache


FLASK_APP_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__
)

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

# Cache
cache = Cache(app)

# Business Logic
from .api_1_0 import api as api_blueprint
app.register_blueprint(api_blueprint)
