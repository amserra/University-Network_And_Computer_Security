import pyqrcode
from io import BytesIO
from requests.utils import requote_uri
import urllib.parse


def generate_qr_code(email,key):
    totp_uri = f'otpauth://totp/SecureAuth:{urllib.parse.quote(email)}?secret={key}&issuer=SecureAuth'

    url = pyqrcode.create(totp_uri)
    stream = BytesIO()
    url.svg(stream, scale=2)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}