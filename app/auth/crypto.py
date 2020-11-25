from Crypto.Random import get_random_bytes 
from werkzeug.security import pbkdf2_bin
import pyqrcode
from io import BytesIO


def generate_secret_totp_key():
    noBytes = 64
    key = get_random_bytes(noBytes) # generates a random secret with noBytes bytes
    key = pbkdf2_bin(key, 'pbkdf2:sha256:150000', 8)
    return key

def generate_qr_code(key):
    totp_uri = f'otpauth://totp?secret={key}'
    url = pyqrcode.create(totp_uri)
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}