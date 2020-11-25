from Crypto.Random import get_random_bytes 
import pyqrcode
from io import BytesIO


def generate_secret_totp_key():
    noBytes = 512
    key = get_random_bytes(noBytes) # generates a random secret with noBytes bytes
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