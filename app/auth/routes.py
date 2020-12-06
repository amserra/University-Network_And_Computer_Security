import logging
logging.basicConfig(level=logging.DEBUG)
from os import urandom

from datetime import datetime as dt, timedelta as td
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from Crypto.Random import get_random_bytes 

from app.models import db, User, BlockedIPs
from .forms import SignupForm, SignInForm, RecoverPasswordForm, Code2FAForm, ChangePasswordForm, MasterPasswordForm
from .crypto import generate_secret_totp_key, totp
from itsdangerous.url_safe import URLSafeSerializer
from ..email.send_email import send_confirmation_email, send_password_recover_email
from .decorators import basic_login_required, full_login_required, return_if_logged, return_if_fully_logged

auth = Blueprint("auth", __name__)

#If a user id is stored in the session, load the user object from the database into ``g.user``.
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    user_id_no2FA = session.get("user_id_no2FA")

    # If both are none, there's no user
    if (user_id is None) and (user_id_no2FA is None):
        g.user = None
    else:
        if user_id is not None:
            g.user = User.query.filter(User.id == user_id).first()
        else:
            # user_id_no2FA is not None
            g.user = User.query.filter(User.id == user_id_no2FA).first()


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
            new_secret_totp_key=generate_secret_totp_key(),
            last_change_key_time=dt.now(),
            created_at=dt.now(),
        )
        db.session.add(new_user)
        db.session.commit()

        logging.debug("Success in POST /register: Created user with email %s" % form.email.data)
        
        send_confirmation_email(form.email.data, form.name.data)
        flash("A confirmation email has been sent to your email.", "info")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/confirm_login", methods=("GET", "POST"))
@auth.route("/confirm_login/<type>", methods=("GET", "POST"))
@basic_login_required
@return_if_fully_logged
def confirm_login(type=None):
    user = g.user
    print(type)
    # Case when a user hasn't a 2FA code and clicks to recover password
    if type and (not user.has_2FA):
        flash("You don't have a 2FA code, so you can't recover your password", "error")
        return redirect(url_for("main.index"))

    print(type)

    #============= TESTE - APAGAR DEPOIS ============
    print(totp(user.secret_totp_key))
    #================================================
    form = Code2FAForm()

    #======== Brute force protection ==========
    if 'attempts_2fa' not in session:
        if(user.brute_force_timestamp_2fa != None):
            time_diference = dt.now() - user.brute_force_timestamp_2fa
            if(time_diference.seconds < 60):
                flash(f"You need to wait {time_diference.seconds} seconds to login. Try again later. Please consider changing password.", "error")
                return redirect(url_for("main.index"))
            else:
                user.brute_force_timestamp_2fa = None
                db.session.commit()
        session['attempts_2fa'] = 5

    if(session['attempts_2fa'] <= 0):
        user.brute_force_timestamp_2fa = dt.now()
        db.session.commit()
        flash("You don't have anymore attempts. Please try again in 1 minute.", "error")
        return redirect(url_for("main.index"))

    if(request.method == 'POST'):
        session['attempts_2fa'] += -1
        flash('Attempts remaining: {}'.format(session['attempts_2fa']), "error")
    # ==========================================

    if form.validate_on_submit():

        if not user.has_2FA:
            user.has_2FA = True
            db.session.commit()
            logging.debug(f"Success in POST /confirm_login: User with email {user.email} used 2FA for the first time")
        
        if type:
            logging.debug("Success in POST /confirm_login/change_password: User %s can now change password" % user.email)
            flash("Correct code. You can now change your password", "info")
            return redirect(url_for("auth.change_password"))
        else:
            session.clear()
            session['user_id'] = user.id
            logging.debug("Success in POST /confirm_login: Logged 2FA user with email %s" % user.email)
            flash("Login successful", "success")
            time = dt.now()
            last_change_key_time = user.last_change_key_time
            time_diference = time - last_change_key_time
            
            if time_diference.days > 365:
                # print("SECONDS")
                # print(f"{time} - {last_change_key_time} = {time_diference.seconds}")
                session["change_secret"] = True
                user.new_secret_totp_key = generate_secret_totp_key()
                return redirect(url_for("qr_code.qrcode", type="change_secret"))


            return redirect(url_for("main.index"))
    
    return render_template("auth/confirm_login.html", form=form, attempts = 'Attempts remaining: {}'.format(session['attempts_2fa']))

# Log in a registered user by adding the user id to the session.
@auth.route("/login", methods=("GET", "POST"))
@return_if_logged
def login():
    form = SignInForm()
        
    
    #======== Brute force protection =========
    if 'attempts_login' not in session:
        ip_info = BlockedIPs.query.filter_by(ip=request.remote_addr).first()
        if(ip_info != None):
            if(dt.now() < ip_info.timeout):
                time_diference = ip_info.timeout - dt.now()
                flash(f"You need to wait {str(time_diference).split('.', 2)[0]} before trying to login", "error")
                return redirect(url_for("main.index"))
        session['attempts_login'] = 10

    if(session['attempts_login'] <= 0):
        session.pop('attempts_login')
        ip_info = BlockedIPs.query.filter_by(ip=request.remote_addr).first()
        if(ip_info == None):
            time = dt.now()
            ip_info = BlockedIPs(
                ip = request.remote_addr, 
                last_timestamp = time,
                timeout = time + td(minutes = 15)
            )
            db.session.add(ip_info)
        else:
            time = dt.now()
            prev_time_diference = ip_info.timeout - ip_info.last_timestamp
            ip_info.last_timestamp = time
            ip_info.timeout = min(time + td(seconds = prev_time_diference.seconds * 2), time + td(hours = 24))
        db.session.commit()
        flash(f"You don't have anymore attempts. Try again in {str(ip_info.timeout - ip_info.last_timestamp).split('.', 2)[0]}", "error")
        return redirect(url_for("main.index"))

    if(request.method == 'POST'):
        session['attempts_login'] += -1
    # ======================================

    if form.validate_on_submit():
        user_id = User.query.filter_by(email=form.email.data).first().id
        session.clear()
        session["user_id_no2FA"] = user_id
        logging.debug("Success in POST /login: Logged(user + password) user with email %s" % form.email.data)

        user = User.query.filter_by(email=form.email.data).first()

        #Unblock IP - Reset brute force protection
        BlockedIPs.query.filter_by(ip=request.remote_addr).delete()
        db.session.commit()
        
        if(not user.email_verified):
            serialized_email = URLSafeSerializer(app.config["SECRET_KEY"]).dumps(user.email)
            return redirect(url_for("email.unconfirmed", user_email=serialized_email))

        if user.has_2FA:
            return redirect(url_for("auth.confirm_login"))
        else:
            return redirect(url_for("qr_code.qrcode"))
    
    if(session['attempts_login'] < 4):
        return render_template("auth/login.html", form=form, attempts = 'Attempts remaining: {}'.format(session['attempts_login']))
    else:
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


@auth.route("/master_password", methods=("GET", "POST"))
@basic_login_required
@return_if_fully_logged
def master_password():
    user = g.user

    #======== Brute force protection ==========
    if 'attempts_master' not in session:
        if(user.brute_force_timestamp_master != None):
            time_diference = dt.now() - user.brute_force_timestamp_master
            day = td(days = 1)
            if(time_diference < day):
                flash(f"You need to wait {str(user.brute_force_timestamp_master + day - dt.now()).split('.', 2)[0]} to recover the 2FA authentication. Please consider changing password.", "error")
                return redirect(url_for("auth.confirm_login"))
            else:
                user.brute_force_timestamp_master = None
                db.session.commit()
        session['attempts_master'] = 5

    if(session['attempts_master'] <= 0):
        user.brute_force_timestamp_master = dt.now()
        db.session.commit()
        flash("You don't have anymore attempts. Please try again in 24 hours.", "error")
        return redirect(url_for("auth.confirm_login"))

    if(request.method == 'POST'):
        session['attempts_master'] += -1
    # ==========================================

    form = MasterPasswordForm()

    if form.validate_on_submit():
        flash("Master password valid. You can now scan the new QR Code", "success")
        user = User.query.filter_by(id=g.user.id).first()
        # Generate a new secret key
        user.has_2FA = False
        user.secret_totp_key = generate_secret_totp_key()
        user.last_change_key_time = dt.now()
        db.session.commit()
        return redirect(url_for("qr_code.qrcode"))

    return render_template("auth/master_password.html", form=form, attempts = 'Attempts remaining: {}'.format(session['attempts_master']))

# Page to change password
@auth.route("/change_password", methods=("GET", "POST"))
@basic_login_required
@return_if_fully_logged
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(id=g.user.id).first()
        user.brute_force_timestamp_master = None        #Reset masterpassword timeout
        user.password = generate_password_hash(form.new_password.data, 'pbkdf2:sha256:150000', 8)
        db.session.commit()
        session.clear()
        flash("Password changed successfully. You can login now", "success")
        return redirect(url_for("main.index"))

    return render_template("auth/change_password.html", form=form)

# Clear the current session, including the stored user id.
@auth.route("/logout")
@full_login_required
def logout():
    session.clear()
    return redirect(url_for("main.index"))

@auth.route("/change_secret")
def change_secret():
    user_id = session.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    user.secret_totp_key = user.new_secret_totp_key
    user.new_secret_totp_key = ""
    user.last_change_key_time = dt.now()
    db.session.commit()
    flash("New qr_code successful", "success")
    return redirect(url_for("main.index"))  