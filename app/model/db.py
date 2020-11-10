import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# Connect to the application's configured database. The connection is unique for each request and will be reused if this is called again.
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db

# If this request connected to the database, close the connection.
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

# Clear existing data and create new tables.
def init_db():
    db = get_db()

    with current_app.open_resource("model/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# Clear existing data and create new tables.
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

# Register database functions with the Flask app. This is called by the application factory.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
