import logging
logging.basicConfig(level=logging.DEBUG)

from datetime import datetime as dt

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from Crypto.Random import get_random_bytes 


from app.models import db, User
from .forms import SignupForm, SignInForm
from .crypto import generate_secret_totp_key, generate_qr_code
from itsdangerous.url_safe import URLSafeSerializer
from ..email.send_email import send_email

auth = Blueprint("auth", __name__)

#If a user id is stored in the session, load the user object from the database into ``g.user``.
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).first()


#Validates that the username is not already taken. Hashes thepassword for security.
@auth.route("/register", methods=("GET", "POST"))
def register():
    if 'user_id' in session:
        return redirect(url_for("main.index"))

    form = SignupForm()

    # validate_on_submit also checks if it is a POST request
    if form.validate_on_submit():

        new_user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=generate_password_hash(form.password.data, 'pbkdf2:sha256:150000', 8),
            created_at=dt.now()
        )
        db.session.add(new_user)
        db.session.commit()

        logging.debug("Success in POST /register: Created user with email %s" % form.email.data)
        
        send_email(form.email.data, form.name.data)
        flash("A confirmation email has been sent to your email.", "info")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/confirm_login", methods=("GET", "POST"))
def confirm_login():
    if 'user_id' in session or 'user_id_no2FA' not in session:
        return redirect(url_for("main.index"))
    
    user = User.query.filter(User.id == session["user_id_no2FA"]).first()

    if user.secret_totp_key is None:
        return redirect(url_for("auth.qr_code"))

    if request.method == "POST":
        user = User.query.filter(User.id == session["user_id_no2FA"]).first()

        code_2FA = request.form["code_2FA"]
        error = None

        if code_2FA != "123456": #just to test
            error = "Code is not correct"
            print(user)
            logging.debug("ERROR in POST /confirm_login: Wrong 2FA code")
        
        if error is None:
            session.clear()
            session['user_id'] = user.id

            logging.debug("Success in POST /confirm_login: Logged 2FA user with email %s" % user.email)
            flash("Login successful", "success")

            return redirect(url_for("main.index"))
        
        flash(error, "error")

    return render_template("auth/confirm_login.html")

# Log in a registered user by adding the user id to the session.
@auth.route("/login", methods=("GET", "POST"))
def login():
    if 'user_id' in session:
        return redirect(url_for("main.index"))

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

        return redirect(url_for("auth.confirm_login", user_id=user.id))

    return render_template("auth/login.html", form=form)

@auth.route("/qrcode")
def qr_code():
    if 'user_id' in session or 'user_id_no2FA' not in session:
        return redirect(url_for("main.index"))
    
    user_id = session.get("user_id_no2FA")
    user = User.query.filter(User.id == user_id).first()

    if user.email_verified != 1:
        flash("Please confirm your email", "error")
        logging.debug(f"ERROR in /qrcode: User with email {user.email} not confirmed")
        return redirect(url_for("main.index"))
    
    if user.secret_totp_key is None:
        return render_template('auth/qr_code.html')

    return redirect(url_for("main.index"))

@auth.route("/generate_qrcode")
def generate_qrcode():
    if 'user_id' in session or 'user_id_no2FA' not in session:
        return redirect(url_for("main.index"))

    user_id = session.get("user_id_no2FA")
    user = User.query.filter(User.id == user_id).first()

    if user.email_verified != 1:
        logging.debug(f"ERROR in /generate_qrcode: User with email {user.email} not confirmed")
        return redirect(url_for("main.index"))

    if user.secret_totp_key is None:
        key = generate_secret_totp_key()
        User.query.filter(User.id == user_id).update(dict(secret_totp_key = key))
        db.session.commit()
        logging.debug(f"SUCCESS in /generate_qrcode: User with email {user.email} activated 2FA")
        session.pop('user_id_no2FA')
        return generate_qr_code(user.secret_totp_key)

    return redirect(url_for("main.index"))


# Clear the current session, including the stored user id.
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))