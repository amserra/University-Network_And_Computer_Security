from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, ValidationError, Regexp
from app.models import db, User

def check_unique(form, field):
    if(User.query.filter_by(email=field.data).first() is not None):
        raise ValidationError('An user with this email already exists')


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
    
