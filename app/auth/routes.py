import functools
import logging
logging.basicConfig(level=logging.DEBUG)

from datetime import datetime as dt
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import db, User
from .forms import SignupForm

auth = Blueprint("auth", __name__)

# View decorator that redirects anonymous users to the login page.
# Add @login_required to pages that can't be accessed by anonymous users
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

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
            created=dt.now()
        )
        db.session.add(new_user)
        db.session.commit()

        logging.debug("Success in POST /register: Created user with email %s" % form.email.data)
        flash("Register successful", "info")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth.route("/confirmLogin", methods=("GET", "POST"))
def confirmLogin():
    if 'user_id' in session:
        return redirect(url_for("main.index"))
    
    if request.method == "POST":
        user_id = request.args.get('user_id')
        user = User.query.filter(User.id == user_id).first()

        code_2FA = request.form["code_2FA"]
        error = None

        if code_2FA != "123456": #just to test
            error = "Code is not correct"
            print(user)
            logging.debug("ERROR in POST /confirmLogin: Wrong 2FA code")
        
        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user.id

            logging.debug("Success in POST /confirmLogin: Logged 2FA user with email %s" % user.email)
            flash("Login successful", "info")

            return redirect(url_for("main.index"))
        
        flash(error, "error")

    return render_template("auth/confirmLogin.html")

# Log in a registered user by adding the user id to the session.
@auth.route("/login", methods=("GET", "POST"))
def login():
    if 'user_id' in session:
        return redirect(url_for("main.index"))
        
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = User.query.filter(User.email == email).first()

        if user is None:
            error = "Incorrect email"
            logging.debug("ERROR in POST /login: Invalid email")
        elif not check_password_hash(user.password, password):
            error = "Incorrect password"
            logging.debug("ERROR in POST /login: Invalid password")
        elif user.email_verified != 0: # quando estiver a funcionar mudar para != para ==
            error = "Check your email in order to verify your account"
            logging.debug("ERROR in POST /login: Email not verified")

        if error is None:
            
            logging.debug("Success in POST /login: Logged(user + password) user with email %s" % email)            
            return redirect(url_for("auth.confirmLogin", user_id=user.id))

        flash(error, "error")

    return render_template("auth/login.html")


# Clear the current session, including the stored user id.
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))