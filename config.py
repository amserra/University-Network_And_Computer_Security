from datetime import timedelta
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ["SECRET_KEY"]
    # Database configurations
    SQLALCHEMY_DATABASE_URI = environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Cookie lifetime
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)
    # Recaptha keys
    RECAPTCHA_PUBLIC_KEY = environ["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY = environ["RECAPTCHA_PRIVATE_KEY"]
    # Email
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USERNAME = environ["MAIL_USERNAME"]
    MAIL_PASSWORD = environ["MAIL_PASSWORD"]
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

class ProdConfig(Config):
    SERVER_NAME = 'secureauth.ml'

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + basedir + "/app/site.sqlite"