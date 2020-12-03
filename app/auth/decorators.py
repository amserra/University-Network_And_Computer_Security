from functools import wraps
from flask import g, redirect, url_for, session, abort

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