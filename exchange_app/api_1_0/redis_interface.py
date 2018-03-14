import redis
import logging
from .. import app
from enum import Enum

class redis_db(Enum):
    BALANCE_OBSERVATION = 0
    TRANSFERS_OBSERVATION_FROM = 1
    TRANSFERS_OBSERVATION_TO = 2


def redis_connect(redisdb):
    return redis.Redis(host = app.config['REDIS_HOST'], port = app.config['REDIS_PORT'], db=redisdb.value)

def get_cont_address(continuation, redisdb):
    db = redis_connect(redisdb)
    addr = db.get(continuation)
    return "" if addr is None else addr.decode()
    
def set_cont_address(continuation, address, redisdb):
    db = redis_connect(redisdb)
    return db.set(continuation, address)
    
def del_cont_address(continuation, redisdb):
    db = redis_connect(redisdb)
    return db.delete(continuation)
    
    
    
def get_cont_address_balances():
    return get_cont_address(redis_db.BALANCE_OBSERVATION)
    
def get_cont_address_transfers_from():
    return get_cont_address(redis_db.TRANSFERS_OBSERVATION_FROM)
    
def get_cont_address_transfers_to():
    return get_cont_address(redis_db.TRANSFERS_OBSERVATION_TO)

    
def set_cont_address_balances():
    return get_cont_address(redis_db.BALANCE_OBSERVATION)

def set_cont_address_transfers_from():
    return get_cont_address(redis_db.TRANSFERS_OBSERVATION_FROM)

def set_cont_address_transfers_to():
    return get_cont_address(redis_db.TRANSFERS_OBSERVATION_TO)
    

def del_cont_address_balances():
    return get_cont_address(redis_db.BALANCE_OBSERVATION)

def del_cont_address_transfers_from():
    return get_cont_address(redis_db.TRANSFERS_OBSERVATION_FROM)

def del_cont_address_transfers_to():
    return get_cont_address(redis_db.TRANSFERS_OBSERVATION_TO)

