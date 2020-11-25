from flask import url_for, render_template
from flask_mail import Message
from os import environ
from app import mail
from .token import generate_confirmation_token

def send_email(to_email, to_name):
    token = generate_confirmation_token(to_email)
    confirm_url = url_for('email.confirm_email', token=token, _external=True)
    html = render_template('email/email_template.html', confirm_url=confirm_url, name=to_name)
    subject = "Please confirm your email"

    msg = Message(
        subject,
        recipients=[to_email],
        html=html,
        sender=environ['MAIL_USERNAME']
    )
    mail.send(msg)