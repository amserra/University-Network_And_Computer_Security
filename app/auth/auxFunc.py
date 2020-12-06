from datetime import datetime as dt

def get_timeout(current_timeout):

    next_timeout = current_timeout * 2

    noBytes = 256
    key = urandom(noBytes).hex() # generates a random secret with noBytes bytes
    return key
