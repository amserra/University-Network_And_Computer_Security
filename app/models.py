"""Data models."""
from . import db

class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(64),
        nullable=False
    )
    email = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False
    )
    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    secret_totp_key = db.Column(
        db.String(512),
        nullable=False
    )
    new_secret_totp_key = db.Column(
        db.String(512)
    )
    has_2FA = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    email_verified_at = db.Column(
        db.DateTime
    )
    master_password = db.Column(
        db.String(512)
    )
    last_change_key_time = db.Column(
        db.DateTime,
        nullable=False
    )
    brute_force_timestamp_2fa = db.Column(
        db.DateTime,
        nullable = True
    )
    brute_force_timestamp_master = db.Column(
        db.DateTime,
        nullable = True
    )

    # What is printed if you print(user). Is a .toString()
    def __repr__(self):
        return "<User {}>".format(self.email)

class BlockedIPs(db.Model):
    """Data model for temporary blocked IPs."""
    __tablename__ = 'blockedIPs'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    ip = db.Column(
        db.String(80),
        nullable = False
    )
    last_timestamp = db.Column(
        db.DateTime,
        nullable = True
    )
    timeout = db.Column(
        db.DateTime,
        nullable = True
    )