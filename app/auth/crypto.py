from os import urandom

def generate_secret_totp_key():
    noBytes = 256
    key = urandom(noBytes).hex() # generates a random secret with noBytes bytes
    print(key)
    return key
