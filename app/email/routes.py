import logging
logging.basicConfig(level=logging.DEBUG)

from datetime import datetime as dt
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from itsdangerous.url_safe import URLSafeSerializer

from app.models import db, User
from .token import generate_confirmation_token, confirm_token
from .send_email import send_email

email = Blueprint("email", __name__)

@email.route('/unconfirmed')
def unconfirmed():
    if request.args.get('user_email') is None:
        return redirect(url_for('main.index'))
    
    user_email = request.args.get('user_email')
    # This prevents someone to harcoding (or URL encoding) an email as request parameter
    try:
        to = URLSafeSerializer(app.config["SECRET_KEY"]).loads(user_email)
    except:
        logging.debug("Exception loading serialization of email in /unconfirmed")
        return redirect(url_for('main.index'))
    
    flash('Please confirm your account', 'info')
    return render_template('email/unconfirmed_email.html', user_email=to)

@email.route('/resend')
def resend_confirmation():
    user_email = request.args.get('user_email')
    user = User.query.filter_by(email=user_email).first_or_404()    
    send_email(user_email, user.name)

    logging.debug("New confirmation email (re)sent to %s" % (user_email))
    flash('A new confirmation email has been sent.', 'info')
    return redirect(url_for('email.unconfirmed'))

@email.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        user_email = confirm_token(token)
    except:
        logging.debug("Exception confirming token: probabily token expired")
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('main.index'))
        
    user = User.query.filter_by(email=user_email).first_or_404()
    if user.email_verified:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_verified = True
        user.email_verified_at = dt.now()
        db.session.add(user)
        db.session.commit()
        logging.debug("Email confirmed in account %s" % (user.email))
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))