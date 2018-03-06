

def build_error(error_message="", failed_items={}):
    
    error_obj = {"errorMessage": error_message,
                    "modelErrors": failed_items
    }
    
    return error_obj

