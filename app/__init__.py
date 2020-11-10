import os
import sys
import logging

from flask import Flask


def create_app(test_config=None):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    # Create and configure an instance of the Flask application.
    app = Flask(__name__, instance_relative_config=True)
    SECRET_KEY = os.environ["SECRET_KEY"]

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    else:
        SECRET_KEY = SECRET_KEY.encode('utf-8', 'surrogatepass') 

    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "db.sqlite"),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        print(str(e))

    # register the database commands
    from app.model import db

    db.init_app(app)

    # apply the blueprints to the app
    from app.controllers import auth, view

    app.register_blueprint(auth.bp)
    app.register_blueprint(view.bp)

    # make url_for('index') == url_for('view.index')
    app.add_url_rule("/", endpoint="index")

    return app
