import logging
logging.basicConfig(level=logging.DEBUG)

from datetime import datetime as dt
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from Crypto.Random import get_random_bytes 

from app.models import db, User
from .forms import SignupForm, SignInForm, RecoverPasswordForm
from .crypto import generate_secret_totp_key
from itsdangerous.url_safe import URLSafeSerializer
from ..email.send_email import send_confirmation_email, send_password_recover_email
from .decorators import basic_login_required, full_login_required, return_if_logged

auth = Blueprint("auth", __name__)

#If a user id is stored in the session, load the user object from the database into ``g.user``.
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).first()

#Validates that the username is not already taken. Hashes the password for security.
@auth.route("/register", methods=("GET", "POST"))
@return_if_logged
def register():
    form = SignupForm()

    # validate_on_submit also checks if it is a POST request
    if form.validate_on_submit():

        new_user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=generate_password_hash(form.password.data, 'pbkdf2:sha256:150000', 8),
            secret_totp_key=generate_secret_totp_key(),
            created_at=dt.now()
        )
        db.session.add(new_user)
        db.session.commit()

        logging.debug("Success in POST /register: Created user with email %s" % form.email.data)
        
        send_confirmation_email(form.email.data, form.name.data)
        flash("A confirmation email has been sent to your email.", "info")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/confirm_login", methods=("GET", "POST"))
@full_login_required
def confirm_login():
    user = User.query.filter(User.id == session["user_id_no2FA"]).first()

    if request.method == "POST":
        user = User.query.filter(User.id == session["user_id_no2FA"]).first()

        code_2FA = request.form["code_2FA"]
        error = None

        if code_2FA != "123456": #just to test
            error = "Code is not correct"
            print(user)
            logging.debug("ERROR in POST /confirm_login: Wrong 2FA code")
        
        if error is None:
            if not user.has_2FA:
                user.has_2FA = True
                db.session.commit()
                logging.debug(f"Success in POST /confirm_login: User with email {user.email} used 2FA for the first time")
            session.clear()
            session['user_id'] = user.id

            logging.debug("Success in POST /confirm_login: Logged 2FA user with email %s" % user.email)
            flash("Login successful", "success")

            return redirect(url_for("main.index"))
        
        flash(error, "error")

    return render_template("auth/confirm_login.html")

# Log in a registered user by adding the user id to the session.
@auth.route("/login", methods=("GET", "POST"))
@return_if_logged
def login():
    form = SignInForm()
        
    if form.validate_on_submit():
        user_id = User.query.filter_by(email=form.email.data).first().id
        session.clear()
        session["user_id_no2FA"] = user_id
        logging.debug("Success in POST /login: Logged(user + password) user with email %s" % form.email.data)

        user = User.query.filter_by(email=form.email.data).first()
        
        if(not user.email_verified):
            serialized_email = URLSafeSerializer(app.config["SECRET_KEY"]).dumps(user.email)
            return redirect(url_for("email.unconfirmed", user_email=serialized_email))

        if user.has_2FA:
            return redirect(url_for("auth.confirm_login"))
        else:
            return redirect(url_for("qr_code.qrcode"))

    return render_template("auth/login.html", form=form)

# If you loose your password you'll have to click the link
# and then introduce your QR code to change the password
@auth.route("/lost_password", methods=("GET", "POST"))
@return_if_logged
def lost_password():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_recover_email(user.email, user.name)
        flash("A recover link has been sent to your email.", "info")

        return redirect(url_for("main.index"))

    return render_template("auth/recover_password.html", form=form)


# Clear the current session, including the stored user id.
@auth.route("/logout")
@full_login_required
def logout():
    session.clear()
    return redirect(url_for("main.index"))