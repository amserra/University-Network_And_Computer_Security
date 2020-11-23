from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session

main = Blueprint("main", __name__)

@main.route("/")
def index():
    if 'user_id' in session:
        msg = "Congrats, you are securely authenticated!"
        return render_template("index.html", msg=msg)

    msg = "Make a secure session!"
    return render_template("index.html", msg=msg)