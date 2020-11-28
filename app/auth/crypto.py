from os import urandom
from werkzeug.security import pbkdf2_bin
import time
import hmac
import hashlib
from base64 import b64encode


def generate_secret_totp_key():
    noBytes = 256
    key = urandom(noBytes).hex() # generates a random secret with noBytes bytes
    return key

def hmac_sha256(key, msg):
    h = hmac.new(key, msg, hashlib.sha256 )
    return h.digest()

def encode_to_base64(string):
    return b64encode(str.encode(string))

def get_digit_power(no_digits):
    result = 1
    for _ in range(no_digits):
        result = result * 10
    return result

def totp(key):
    no_digits = 6
    key_kdf = pbkdf2_bin(key,"salt",100)
    unix_timestamp = int(time.time())

    step = str(unix_timestamp//30)
    
    while len(step) < 16:
        step = '0' + step
    step = encode_to_base64(step)
    hash = hmac_sha256(key_kdf, step)
    offset = hash[len(hash) - 1] & 0xf

    binary = ((hash[offset] & 0x7f) << 24) | ((hash[offset + 1] & 0xff) << 16) | ((hash[offset + 2] & 0xff) << 8) | (hash[offset + 3] & 0xff)

    otp = binary % get_digit_power(no_digits)

    result = str(otp)

    while len(result) < no_digits:
        result = '0' + result

    return result

