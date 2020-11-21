from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session

from werkzeug.exceptions import abort

from app.controllers.auth import login_required
from app.model.db import get_db

bp = Blueprint("view", __name__)

@bp.route("/")
def index():
    if 'user_id' in session:
        msg = "Congrats, you are securely authenticated!"
        return render_template("index.html", msg=msg)

    msg = "Make a secure session!"
    return render_template("index.html", msg=msg)