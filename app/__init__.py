from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Logging setup. Disables unecessary logs
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")

    # Initialize the database
    db.init_app(app)

    # apply the blueprints to the app
    from app.main.routes import main
    from app.auth.routes import auth
    from app.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(errors)

    with app.app_context():
        # Creates database tables
        db.create_all(app=app)
        return app
