import logging
logging.basicConfig(level=logging.DEBUG)

from datetime import datetime as dt
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from itsdangerous.url_safe import URLSafeSerializer

from app.models import db, User
from .generate_qr_code import generate_qr_code


qr_code = Blueprint("qr_code", __name__)

@qr_code.route("/qrcode/<type>")
@qr_code.route("/qrcode")
def qrcode(type=None):
    if type == "change_secret" and "change_secret" in session:
        msg = "For security reasons we advise you to scan a new qr code on your app"
        return render_template('qr_code/qr_code.html', msg=msg, change_secret=True)

    if 'user_id' in session or 'user_id_no2FA' not in session:
        return redirect(url_for("main.index"))
    
    user_id = session.get("user_id_no2FA")
    user = User.query.filter(User.id == user_id).first()

    if not user.has_2FA:
        msg = "Open your phone app and scan the following QR Code:"
        return render_template('qr_code/qr_code.html', msg=msg, change_secret=False)

    return redirect(url_for("main.index"))

@qr_code.route("/generate_qrcode")
def generate_qrcode():
    if 'change_secret' in session:
        user_id = session.get("user_id")
        user = User.query.filter(User.id == user_id).first()
        session.pop("change_secret")
        return generate_qr_code(user.email,user.new_secret_totp_key)

    if 'user_id' in session or 'user_id_no2FA' not in session:
        return redirect(url_for("main.index"))

    user_id = session.get("user_id_no2FA")
    user = User.query.filter(User.id == user_id).first()

    if not user.has_2FA:
        return generate_qr_code(user.email,user.secret_totp_key)

    return redirect(url_for("main.index"))
