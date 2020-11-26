from flask import url_for, render_template
from flask_mail import Message
from os import environ
from app import mail
from .token import generate_token

def send_confirmation_email(to_email, to_name):
    token = generate_token(to_email)
    url = url_for('email.confirm_email', token=token, _external=True)
    html = render_template('email/confirmation_email_template.html', url=url, name=to_name)
    subject = "Please confirm your email"

    msg = Message(
        subject,
        recipients=[to_email],
        html=html,
        sender=environ['MAIL_USERNAME']
    )
    mail.send(msg)

def send_password_recover_email(to_email, to_name):
    token = generate_token(to_email)
    url = url_for('email.recover_password', token=token, _external=True)
    html = render_template('email/recover_password_template.html', url=url, name=to_name)
    subject = "Recover password"

    msg = Message(
        subject,
        recipients=[to_email],
        html=html,
        sender=environ['MAIL_USERNAME']
    )
    mail.send(msg)