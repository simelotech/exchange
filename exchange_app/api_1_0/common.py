import os
import hashlib

def build_error(error_message="", failed_items={}):
    """
    Generate error message for output
    """
    error_obj = {"errorMessage": error_message,
                    "modelErrors": failed_items
    }
    
    return error_obj
   
   
def generate_hash_key():
    """
    Generate new random hash to be used as key
    """
    m = hashlib.sha256()
    m.update(os.urandom(64))
    return m.hexdigest()


