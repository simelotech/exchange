from flask import Blueprint

api = Blueprint('api', __name__)

from . import address, wallets, assets, capabilities, isalive, balances, history, transactions
