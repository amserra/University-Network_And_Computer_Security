from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session

main = Blueprint("main", __name__)

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