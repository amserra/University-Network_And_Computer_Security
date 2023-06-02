from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session
from app.models import db, User

main = Blueprint("main", __name__)

@main.before_app_request
def check_password_change():
    if 'inputted_password' in session and 'user_id' in session:
        inputted_password = session.get('inputted_password')
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        if user.password != inputted_password:
            flash('Session remotely closed by the user', 'error')
            session.clear()
            return redirect(url_for('main.index'))

@main.route("/")
def index():
    # If the user was a partially authenticated user and clicked "Home", is as if he logged out
    if 'user_id_no2FA' in session:
        session.clear()
    
    if 'user_id' in session:
        msg = "Congrats, you are securely authenticated!"
        return render_template("index.html", msg=msg)

    msg = "Make a secure session!"
    return render_template("index.html", msg=msg)