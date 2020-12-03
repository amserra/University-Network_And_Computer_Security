from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, ValidationError, Regexp
from werkzeug.security import check_password_hash
from app.models import db, User
from flask import g
from .crypto import totp

def check_unique(form, field):
    if(User.query.filter_by(email=field.data).first() is not None):
        raise ValidationError('An user with this email already exists')

def check_existence(form, field):
    if(User.query.filter_by(email=field.data).first() is None):
        raise ValidationError('No such email registered')

class SignupForm(FlaskForm):
    name = StringField(
        "Name", [DataRequired(message="Enter a name")]
    )
    email = EmailField(
        "Email", [Email(message="Not a valid email address"), check_unique]
    )
    password = PasswordField(
        "Password",
        [
            DataRequired(message="Please enter a password"),
            Length(min=8, max=40, message="Must be at least 8 characters"),
            Regexp(regex=".*[$&+,:;=?@#!].*", message="Must have at least one special symbol"),
            Regexp(regex=".*[A-Z].*", message="Must have at least one capital letter"),
            Regexp(regex=".*[0-9].*", message="Must have be at least one number")
            
        ],
    )
    confirmPassword = PasswordField(
        "Repeat Password", [
            DataRequired(message="Please repeat your password"),
            EqualTo('password', message="Passwords must match")]
    )

    recaptcha = RecaptchaField()
    
def check_email_exists(form, field):
    if(User.query.filter_by(email=field.data).first() is None):
        raise ValidationError('The email or password is incorrect')

def check_password_matches(form, field):
    user = User.query.filter_by(email=form.email.data).first()

    if(user is not None):
        result = check_password_hash(user.password, field.data)
        if(not result):
            raise ValidationError('The email or password is incorrect')
    else:
        raise ValidationError('The email or password is incorrect')

def check_code_matches(form, field):
    user = g.user

    if(field.data != totp(user.secret_totp_key)):
        raise ValidationError('The code is incorrect')
    

class SignInForm(FlaskForm):
    email = StringField(
        "Email", [DataRequired(message="Enter an email address"), check_email_exists]
    )
    password = PasswordField(
        "Password",[DataRequired(message="Enter a password"), check_password_matches],
    )

class RecoverPasswordForm(FlaskForm):
    email = StringField(
        "Email", [DataRequired(message="Enter an email address"), check_existence]
    )

class Code2FAForm(FlaskForm):
    code_2FA = StringField(
        "code_2FA", [DataRequired(message="Enter a six digit code"), check_code_matches]
    )

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("new_password", [
        DataRequired(message="Please enter a new password"),
        Length(min=8, max=40, message="Must be at least 8 characters"),
        Regexp(regex=".*[$&+,:;=?@#!].*", message="Must have at least one special symbol"),
        Regexp(regex=".*[A-Z].*", message="Must have at least one capital letter"),
        Regexp(regex=".*[0-9].*", message="Must have be at least one number")])
    confirm_new_password = PasswordField("confirm_new_password", [
        DataRequired(message="Please repeat your password"),
        EqualTo('new_password', message="Passwords must match")])

def check_master_password(form, field):
    user = g.user
    
    if not check_password_hash(user.master_password, field.data):
        raise ValidationError('The master password is incorrect')

class MasterPasswordForm(FlaskForm):
    master_password = PasswordField("master_password", [
        DataRequired(message="Please introduce the master password"),
        check_master_password])