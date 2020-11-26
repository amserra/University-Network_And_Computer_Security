from Crypto.Random import get_random_bytes 

def generate_secret_totp_key():
    noBytes = 256
    key = get_random_bytes(noBytes) # generates a random secret with noBytes bytes
    return key

