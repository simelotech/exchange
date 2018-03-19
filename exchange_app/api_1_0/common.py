import os
import hashlib
from enum import Enum

class error_codes(Enum):
    unknown = 1
    amountIsTooSmall = 2
    notEnoughBalance = 3

<<<<<<< HEAD

def build_error(error_message="", error_code = error_codes.unknown, failed_items={}):
    """
    Generate error message for output
    """
    error_obj = {"errorMessage": error_message,
                 "errorCode": error_code.name,
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

=======
def build_error(error_message="", failed_items={}):

    error_obj = {
        "errorMessage": error_message,
        "modelErrors": failed_items
    }
>>>>>>> 6c22cfc36b6b953eb43b7c69d9249aff8d740a36

    return error_obj
