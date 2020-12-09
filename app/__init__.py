from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_simple_geoip import SimpleGeoIP
from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app

# Logging setup. Disables unecessary logs
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

db = SQLAlchemy()
mail = Mail()
simple_geoip = SimpleGeoIP()

def create_app():
    
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")

    # Initialize the database
    db.init_app(app)
    mail.init_app(app)
    simple_geoip.init_app(app)

    # apply the blueprints to the app
    from app.main.routes import main
    from app.auth.routes import auth
    from app.email.routes import email
    from app.qr_code.routes import qr_code
    from app.errors.handlers import errors
    from app.api.routes import api
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(email)
    app.register_blueprint(qr_code)
    app.register_blueprint(errors)
    app.register_blueprint(api, url_prefix='/api')
    
    @app.after_request
    def responde_headers(response):
        response.headers['X-Content-Type-Options'] = "nosniff"
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    with app.app_context():
        # Creates database tables
        db.create_all(app=app)
        return app



    
