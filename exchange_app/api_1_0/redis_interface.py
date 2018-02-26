import redis
import logging
from .. import app

def redis_connect():
    return redis.Redis(host='192.168.56.101', port=6379, db=0) #TODO: get this from app settings url

def get_cont_address(continuation):
    redis_db = redis_connect()
    addr = redis_db.get(continuation)
    return "" if addr is None else addr.decode()
    
def set_cont_address(continuation, address):
    redis_db = redis_connect()
    redis_db.set(continuation, address)
    
def del_cont_address(continuation):
    redis_db = redis_connect()
    redis_db.delete(continuation)
    