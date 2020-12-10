from functools import wraps
from flask import g, redirect, url_for, session, abort, request, flash
from datetime import datetime as dt
from app.models import BlockedIPs
from .auxFunc import getIP

def return_if_logged(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if ('user_id' in session) or ('user_id_no2FA' in session):
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function

def return_if_fully_logged(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function

def basic_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id_no2FA' not in session:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def full_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def check_ip_banned(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = getIP(request)
        ip_info = BlockedIPs.query.filter_by(ip=ip).first()
        if (ip_info != None and dt.now() < ip_info.timeout):
            time_diference = ip_info.timeout - dt.now()
            flash(f"You need to wait {str(time_diference).split('.', 2)[0]} before trying this operation again", "error")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function