import pyqrcode
from io import BytesIO

def generate_qr_code(key):
    totp_uri = f'otpauth://totp?secret={key}'
    url = pyqrcode.create(totp_uri)
    stream = BytesIO()
    url.svg(stream, scale=2)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}