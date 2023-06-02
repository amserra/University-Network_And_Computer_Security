from flask import url_for, render_template
from flask_mail import Message
from os import environ
from app import mail
from .token import generate_token, generate_token_with_id

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

def send_master_password_email(to_email, to_name, master_password):
    html = render_template('email/master_password_template.html', name=to_name, master_password=master_password)
    subject = "Master password"

    msg = Message(
        subject,
        recipients=[to_email],
        html=html,
        sender=environ['MAIL_USERNAME']
    )
    mail.send(msg)

def send_alert_unknown_machine(to_email, to_name, user_agent, city, machine_id):
    token = generate_token_with_id(to_email, machine_id)
    url = url_for('auth.change_password_token', token=token, _external=True)
    html = render_template('email/alert_unknown_machine.html', name=to_name, user_agent=user_agent, city=city, url=url)
    subject = "Alert - Unknown machine logged into your account"

    msg = Message(
        subject,
        recipients=[to_email],
        html=html,
        sender=environ['MAIL_USERNAME']
    )
    mail.send(msg)

def send_alert_unknown_machine_basic(to_email, to_name, user_agent, city):
    html = render_template('email/alert_unknown_machine_basic.html', name=to_name, user_agent=user_agent, city=city)
    subject = "Alert - Unknown machine introduced your password"

    msg = Message(
        subject,
        recipients=[to_email],
        html=html,
        sender=environ['MAIL_USERNAME']
    )
    mail.send(msg)