import functools
import logging

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
### TODO: Define generate_password_hash method

from app.model.model import db_get_user_by_id, db_get_user_by_email, db_create_user

from app.classes.forms import SignupForm

logging.basicConfig(level=logging.DEBUG)
bp = Blueprint("auth", __name__)


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
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (db_get_user_by_id(user_id))


#Validates that the username is not already taken. Hashes thepassword for security.
@bp.route("/register", methods=("GET", "POST"))
def register():
    if 'user_id' in session:
        return redirect(url_for("index"))

    form = SignupForm()

    # validate_on_submit also checks if it is a POST request
    if form.validate_on_submit():
        # Missing validation with database (check against existing emails)
        db_create_user(form.name.data, form.email.data, generate_password_hash(form.password.data))
        logging.debug("Success in POST /register: Created user with email %s" % form.email.data)
        flash("Register successful", "info")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


# Log in a registered user by adding the user id to the session.
@bp.route("/login", methods=("GET", "POST"))
def login():
    if 'user_id' in session:
        return redirect(url_for("index"))
        
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = (db_get_user_by_email(email))

        if user is None:
            error = "Incorrect email"
            logging.debug("ERROR in POST /login: Invalid email")
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"
            logging.debug("ERROR in POST /login: Invalid password")

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]

            logging.debug("Success in POST /login: Logged user with email %s" % email)
            flash("Login successful", "info")
            
            return redirect(url_for("index"))

        flash(error, "error")

    return render_template("auth/login.html")


# Clear the current session, including the stored user id.
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))